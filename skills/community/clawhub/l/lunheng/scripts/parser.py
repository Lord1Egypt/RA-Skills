"""
pipeline/parser.py — 案情要素解析模块
从 pipeline.py 拆分而来 (2026-07-18)
职责：案情描述 → 结构化要素 (CaseElements)
"""

import json
import os
import re
import sys
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from error_utils import retry_with_backoff, log_error, log_warning

# ─── API 配置（从统一配置模块导入）───────────────
from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL


# ─── 数据结构 ──────────────────────────────────────────
@dataclass
class CaseElements:
    """从案情描述中解析出的结构化要素"""
    cause: str = ""
    parties: dict = field(default_factory=dict)
    claims: list = field(default_factory=list)
    facts: list = field(default_factory=list)
    disputes: list = field(default_factory=list)
    evidence: list = field(default_factory=list)
    legal_issues: list = field(default_factory=list)
    applicable_laws: list = field(default_factory=list)
    raw_text: str = ""


# ─── 案由→法律映射 ─────────────────────────────────────
CAUSE_LAW_MAP = {
    "民间借贷": {"laws": ["民法典第667-680条", "最高人民法院关于审理民间借贷案件适用法律若干问题的规定"], "primary": "借款合同"},
    "买卖合同": {"laws": ["民法典第595-646条"], "primary": "买卖合同"},
    "租赁合同": {"laws": ["民法典第703-734条"], "primary": "租赁合同"},
    "建设工程": {"laws": ["民法典第788-808条", "最高法建设工程司法解释"], "primary": "建设工程合同"},
    "劳动合同": {"laws": ["劳动合同法", "劳动法"], "primary": "劳动合同"},
    "离婚纠纷": {"laws": ["民法典第1076-1092条"], "primary": "婚姻家庭"},
    "交通事故": {"laws": ["道路交通安全法", "民法典第1179-1187条"], "primary": "机动车交通事故责任"},
    "侵权责任": {"laws": ["民法典第1164-1187条"], "primary": "侵权责任"},
    "房屋买卖": {"laws": ["民法典第595-646条", "城市房地产管理法"], "primary": "房屋买卖合同"},
    "物业服务": {"laws": ["民法典第937-950条"], "primary": "物业服务合同"},
    "著作权": {"laws": ["著作权法", "著作权法实施条例"], "primary": "著作权"},
    "专利权": {"laws": ["专利法", "专利法实施细则"], "primary": "专利权"},
    "商标权": {"laws": ["商标法", "商标法实施条例"], "primary": "商标权"},
    "公司决议": {"laws": ["公司法第22条"], "primary": "公司决议"},
    "行政处罚": {"laws": ["行政处罚法"], "primary": "行政处罚"},
    "行政许可": {"laws": ["行政许可法"], "primary": "行政许可"},
    "确认合同效力": {"laws": ["民法典第144-157条"], "primary": "合同效力"},
    "医疗损害": {"laws": ["民法典第1218-1228条", "医疗纠纷预防和处理条例"], "primary": "医疗损害责任"},
    "保险合同": {"laws": ["保险法"], "primary": "保险合同"},
    "不当得利": {"laws": ["民法典第985-988条"], "primary": "不当得利"},
    "无因管理": {"laws": ["民法典第979-984条"], "primary": "无因管理"},
    "保证合同": {"laws": ["民法典第681-702条"], "primary": "保证合同"},
    "定金合同": {"laws": ["民法典第586-590条"], "primary": "定金"},
}


# ─── LLM 解析 ──────────────────────────────────────────
SYSTEM_PROMPT = """你是法律助手。从案情描述中提取结构化要素，输出JSON格式：
{"cause": "案由", "parties": {"原告": [], "被告": [], "第三人": []}, "claims": [], "facts": [], "disputes": [], "evidence": [], "legal_issues": [], "applicable_laws": []}

提取规则：
1. 案由：准确识别，参考《民事案件案由规定》
2. 当事人：区分原告/被告/第三人
3. 诉讼请求：具体事项（金额、行为）
4. 关键事实：时间、地点、行为、金额
5. 争议焦点：原被告核心分歧
6. 证据：类型和内容
7. 法律问题：争议点
8. 适用法条：法律名称+条款号

只输出JSON，不要其他内容。信息不足返回空数组[]。"""


def llm_parse_elements(text: str, cause_hint: str = '') -> Optional[CaseElements]:
    """使用 LLM 解析案情要素（含重试）"""
    if not LLM_API_KEY:
        log_warning("parser", "llm_parse_elements", "LLM API key 未配置，跳过 LLM 解析")
        return None

    user_msg = SYSTEM_PROMPT + "\n\n案情描述：\n" + text
    if cause_hint:
        user_msg = SYSTEM_PROMPT + "\n\n案由提示：" + cause_hint + "\n\n案情描述：\n" + text

    body = json.dumps({
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": user_msg}],
        "temperature": 0.1,
        "max_tokens": 4000,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{LLM_BASE_URL}/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            print("  🤖 调用 LLM 解析要素...", file=sys.stderr)
            resp = urllib.request.urlopen(req, timeout=30)
            data = json.loads(resp.read())
            content = data["choices"][0]["message"]["content"]

            # 调试：打印 LLM 返回内容
            print(f"  🔍 LLM 返回内容前200字符: {content[:200]}", file=sys.stderr)

            json_match = re.search(r'\{[\s\S]*\}', content)
            if not json_match:
                log_warning("parser", "llm_parse_elements", "LLM 返回内容中未找到 JSON")
                return None

            json_str = json_match.group()
            print(f"  🔍 提取的 JSON 前200字符: {json_str[:200]}", file=sys.stderr)
            
            # 尝试修复常见 JSON 语法错误
            json_str = re.sub(r',\s*([}\]])', r'\1', json_str)  # 移除尾随逗号
            json_str = re.sub(r'\n\s*\n', '\n', json_str)  # 移除多余空行
            
            try:
                parsed = json.loads(json_str)
            except json.JSONDecodeError as e:
                log_warning("parser", "llm_parse_elements", f"JSON 解析失败: {e}")
                print(f"  🔍 JSON 解析错误位置: {json_str[max(0,e.pos-20):e.pos+20]}", file=sys.stderr)
                # 尝试更激进的修复
                json_str = re.sub(r"'([^']*)':", r'"\1":', json_str)  # 单引号转双引号
                json_str = re.sub(r',\s*([}\]])', r'\1', json_str)  # 再次移除尾随逗号
                try:
                    parsed = json.loads(json_str)
                except json.JSONDecodeError:
                    log_warning("parser", "llm_parse_elements", "JSON 修复失败")
                    return None

            elements = CaseElements(
                cause=parsed.get("cause", ""),
                parties=parsed.get("parties", {}),
                claims=parsed.get("claims", []),
                facts=parsed.get("facts", []),
                disputes=parsed.get("disputes", []),
                evidence=parsed.get("evidence", []),
                legal_issues=parsed.get("legal_issues", []),
                applicable_laws=parsed.get("applicable_laws", []),
                raw_text=text,
            )

            if not elements.cause:
                log_warning("parser", "llm_parse_elements", "LLM 未识别案由")
                return None

            print(f"  ✅ LLM 解析成功: 案由={elements.cause}, "
                  f"当事人={sum(len(v) for v in elements.parties.values())}人, "
                  f"事实={len(elements.facts)}条, "
                  f"争议={len(elements.disputes)}个", file=sys.stderr)

            return elements

        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries:
                delay = 2 ** attempt
                log_warning("parser", "llm_parse_elements", f"429 限流，{delay}s 后重试")
                import time
                time.sleep(delay)
                continue
            log_error("parser", "llm_parse_elements", e, {"http_code": e.code})
            return None
        except Exception as e:
            log_error("parser", "llm_parse_elements", e)
            return None

    return None


# ─── 正则解析 (fallback) ───────────────────────────────
CAUSE_KEYWORDS = {
    "民间借贷": ["借款", "借贷", "借条", "欠款", "利息", "还款", "出借"],
    "买卖合同": ["买卖", "购销", "供货", "退货", "质量", "货款"],
    "租赁合同": ["租赁", "房租", "租金", "承租", "出租"],
    "建设工程": ["工程", "施工", "建设", "工程款", "结算"],
    "劳动合同": ["劳动", "工资", "社保", "解除劳动合同", "经济补偿"],
    "离婚纠纷": ["离婚", "财产分割", "子女抚养"],
    "交通事故": ["交通事故", "车祸", "撞", "交强险", "损害赔偿"],
    "侵权责任": ["侵权", "损害赔偿", "人身损害", "财产损害"],
    "确认合同效力": ["合同效力", "无效合同", "可撤销"],
    "公司决议": ["股东会", "董事会", "公司决议"],
    "著作权": ["著作权", "版权", "抄袭", "侵权作品"],
    "专利权": ["专利", "发明专利", "实用新型", "外观设计"],
    "商标权": ["商标", "注册商标", "商标侵权"],
    "行政处罚": ["行政处罚", "罚款", "吊销许可证"],
    "房屋买卖": ["房屋买卖", "购房", "过户", "房产"],
    "物业服务": ["物业", "物业费", "物业服务"],
    "医疗损害": ["医疗", "医院", "诊疗", "医疗事故"],
    "不当得利": ["不当得利", "没有合法根据", "获得利益"],
    "保证合同": ["保证", "担保", "连带责任"],
}


def _detect_cause(text: str) -> str:
    """自动识别案由"""
    text_lower = text.lower()
    scores = {}
    for cause, keywords in CAUSE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[cause] = score
    if scores:
        return max(scores, key=scores.get)
    return "民事纠纷"


def _extract_parties(text: str) -> dict:
    """提取当事人信息（支持自然人 + 法人/公司）"""
    parties = {"原告": [], "被告": [], "第三人": []}

    # 公司/法人名称模式：含"公司""集团""银行""医院"等，允许括号、数字，后缀后可跟分/支行
    _CORP = r'[\u4e00-\u9fa5（）()\d]{2,40}(?:有限公司|股份有限公司|集团|银行|医院|学校|基金会|协会|合作社|事务所)[\u4e00-\u9fa5]*'
    # 自然人姓名模式：纯中文 2-6 字
    _PERSON = r'[\u4e00-\u9fa5]{2,6}'
    _NAME = f'(?:{_CORP}|{_PERSON})'

    for role in ["原告", "被告", "第三人"]:
        patterns = [
            # 模式1: "原告：XXX" 或 "原告:XXX"
            rf'{role}[：:]\s*({_NAME})',
            # 模式2: "原告XXX与被告XXX"
            rf'{role}({_NAME})(?:与|诉至|诉|和)',
            rf'{role}({_NAME})(?:系|为|向)',
            rf'{role}({_NAME})(?:因|向|借款|签|支付|转账|催要|提起)',
            # 模式3: "被告李四民间借贷纠纷一案" — 名字后跟案由/一案
            rf'{role}({_NAME})(?:一案|纠纷|民间借贷|买卖合同|租赁合同|离婚|交通事故|侵权|劳动争议|继承)',
            # 模式4: "被告陈某、赵某" — 名字后跟顿号（多个当事人）
            rf'{role}({_NAME})、',
            # 模式5: "原告张三。" — 名字后跟句号
            rf'{role}({_NAME})[。；，]',
        ]
        for pat in patterns:
            matches = re.findall(pat, text)
            for m in matches:
                name = m.strip()
                # 截断干扰词（案由 + 常见后缀）
                name = re.split(r'民间借贷|纠纷|一案|合同|买卖|租赁|侵权|诉讼|刑事|民事|离婚|交通事故|劳动争议|继承|不当得利|保证合同|物业服务|公司决议|医疗损害|建设工程|借款|签|支付|转账|催要|提起', name)[0]
                if len(name) < 2:
                    continue
                # 公司名：允许较长，含括号/数字
                is_corp = bool(re.search(r'公司|集团|银行|医院|学校|基金会|协会|合作社|事务所', name))
                max_len = 40 if is_corp else 6
                if len(name) > max_len:
                    continue
                if name in parties[role]:
                    continue
                # 排除干扰词（仅对自然人名，公司名不过滤）
                if not is_corp:
                    # 通用干扰词
                    if re.search(r'系|为|向|朋友|与|诉|和|但|而|于|因|在|的|一案|纠纷|多次|停止|支付|签订|转账|催要|提起|借款|归还|本金|利息|约定|期限|利率|银行|方式|账户|万元|人民币|承担|本案|诉讼|费用|以|根据|驾驶|骑|发生|负|构成|误将|操作|损害|知情', name):
                        continue
                    if not re.match(r'^[\u4e00-\u9fa5]+$', name):
                        continue
                    # 名字不应以常见动词/介词开头
                    if re.match(r'^[以根据因在从对向把被]', name):
                        continue
                    # 名字不应重复（如“公司公司决议”）
                    if re.match(r'(.{2,})\1', name):
                        continue
                parties[role].append(name)

    # 后处理：提取顿号分隔的多个当事人（如“被告陈某、赵某”）
    for role in ["原告", "被告", "第三人"]:
        if not parties[role]:
            continue
        for existing_name in list(parties[role]):
            # 在原文中找到已识别名字后面的顿号+名字
            esc = re.escape(existing_name)
            cont_pat = rf'{esc}[、，]({_NAME})'
            for m in re.finditer(cont_pat, text):
                extra = m.group(1).strip()
                # 截断案由干扰词
                extra = re.split(r'民间借贷|纠纷|一案|合同|买卖|租赁|侵权|诉讼|刑事|民事', extra)[0]
                if extra not in parties[role] and len(extra) >= 2:
                    is_corp = bool(re.search(r'公司|集团|银行|医院|学校', extra))
                    if is_corp or (re.match(r'^[\u4e00-\u9fa5]+$', extra) and len(extra) <= 6):
                        parties[role].append(extra)

    # 补充提取被告（当原告已识别但被告缺失时）
    if parties["原告"] and not parties["被告"]:
        for pat in [
            rf'诉(?:被告)?({_NAME})(?:一案|纠纷|,|，)',
            rf'与(?:被告)?({_NAME})(?:一案|纠纷|,|，)',
        ]:
            matches = re.findall(pat, text)
            for m in matches:
                name = m.strip()
                name = re.split(r'民间借贷|纠纷|一案|合同|买卖|租赁|侵权|诉讼|刑事|民事|离婚|交通事故|劳动争议|继承|不当得利|保证合同|物业服务|公司决议|医疗损害|建设工程', name)[0]
                if len(name) < 2:
                    continue
                is_corp = bool(re.search(r'公司|集团|银行|医院|学校', name))
                max_len = 40 if is_corp else 6
                if len(name) > max_len:
                    continue
                if name in parties["被告"] or name in parties["原告"]:
                    continue
                if not is_corp:
                    if re.search(r'一案|纠纷|的|在|因', name):
                        continue
                    if not re.match(r'^[\u4e00-\u9fa5]+$', name):
                        continue
                parties["被告"].append(name)
            if parties["被告"]:
                break

    return parties


def _extract_claims(text: str) -> list:
    """提取诉讼请求"""
    claims = []
    match = re.search(r'诉讼请求[::\s]*(.+?)(?=(?:事实|理由|此致|此上|证据|$))', text, re.DOTALL)
    if match:
        claim_text = match.group(1)
        items = re.split(r'\n\s*\d+[.、))]\s*', claim_text)
        claims = [item.strip() for item in items if item.strip() and len(item.strip()) > 3]

    if not claims:
        raw = re.findall(r'请求[^。]*?(?:判令|判决|支持)[^。]+', text)
        for r in raw:
            body = re.sub(r'^请求[^::]*[::]?\s*', '', r)
            items = re.split(r'\d+[.、))]\s*', body)
            for item in items:
                item = item.strip().rstrip(';;,, ')
                if item and len(item) > 3:
                    claims.append(item)

    return claims[:10]


def _extract_facts(text: str) -> list:
    """提取关键事实"""
    facts = []
    exclude_pat = re.compile(r'(?:诉讼请求|请求判令|请求支付|请求被告|本案诉讼|判令|判决|原告认为|被告认为|被告辩称|被告偿|被告支付|原告请求)')

    for pattern in [
        r'(?:经审理查明|本院认定|经查明|案件事实|查明)[::\s]*(.+?)(?=(?:本院认为|判决如下|综上|以上事实|证据|原告主张|被告抗辩|$))',
        r'(?:事实与理由)[::\s]*(.+?)(?=(?:本院认为|判决如下|综上|$))',
        r'(?:事情经过|事情经过如下)[::\s]*(.+?)(?=(?:原告|被告|综上|$))',
    ]:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            fact_text = match.group(1)
            items = re.split(r'[。;\n]', fact_text)
            facts = [item.strip() for item in items if item.strip() and len(item.strip()) > 8 and not exclude_pat.search(item)]
            break

    if not facts:
        sentences = re.split(r'[。;\n]', text)
        for s in sentences:
            s = s.strip()
            if len(s) < 10:
                continue
            if exclude_pat.search(s):
                continue
            if re.search(r'\d{4}年|万元|元|借|还|签|付|交|约定|到期|违约|死亡|受伤|事故|转账|偿还', s):
                facts.append(s)

    return facts[:15]


def _extract_disputes(text: str) -> list:
    """提取争议焦点"""
    disputes = []
    match = re.search(r'(?:争议焦点|争点|焦点问题|双方争议)[::\s]*(.+?)(?=(?:本院认为|事实|判决|综上|$))', text, re.DOTALL)
    if match:
        items = re.split(r'\n\s*\d+[.、))]\s*', match.group(1))
        disputes = [item.strip() for item in items if item.strip() and len(item.strip()) > 5]

    if not disputes:
        patterns = [
            r'(?:双方|原被告)(?:对|就)[^。]{5,40}(?:存在|有)(?:争议|分歧|异议)',
            r'被告(?:认为|辩称|主张|抗辩)[^。]{5,50}',
            r'(?:核心|主要|本案)(?:争议|分歧|焦点)(?:在于|是)[^。]+',
        ]
        for pat in patterns:
            matches = re.findall(pat, text)
            disputes.extend([m.strip() for m in matches if len(m.strip()) > 8])

    return disputes[:8]


def _extract_evidence(text: str) -> list:
    """提取证据信息"""
    evidence = []
    match = re.search(r'(?:证据|证据清单|主要证据)[::\s]*(.+?)(?=(?:事实|理由|本院认为|判决|$))', text, re.DOTALL)
    if match:
        items = re.split(r'\n\s*\d+[.、))]\s*', match.group(1))
        evidence = [item.strip() for item in items if item.strip() and len(item.strip()) > 5]
    return evidence[:10]


def _identify_legal_issues(text: str, cause: str) -> list:
    """识别涉及的法律问题"""
    issues = []
    general_issues = {
        "合同效力": ["合同效力", "无效", "可撤销", "显失公平", "胁迫", "欺诈"],
        "违约责任": ["违约", "违约金", "损害赔偿", "继续履行"],
        "诉讼时效": ["时效", "诉讼时效", "时效中断", "时效中止"],
        "举证责任": ["举证", "举证责任", "证据不足", "证明标准"],
        "管辖权": ["管辖", "管辖权", "异地起诉"],
        "利息计算": ["利息", "利率", "罚息", "复利"],
        "担保责任": ["担保", "保证", "抵押", "质押"],
        "合同解除": ["解除合同", "合同解除", "解除权"],
    }
    for issue, keywords in general_issues.items():
        if any(kw in text for kw in keywords):
            issues.append(issue)
    return issues[:8]


def _get_applicable_laws(cause: str) -> list:
    """根据案由获取适用法条"""
    for key, info in CAUSE_LAW_MAP.items():
        if key in cause:
            return info["laws"]
    for key, info in CAUSE_LAW_MAP.items():
        if any(kw in cause for kw in [key, info["primary"]]):
            return info["laws"]
    return ["民法典"]


# ─── 说理模板加载 ──────────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data" / "shape_spirit"
TEMPLATES_PATH = DATA_DIR / "reasoning_templates.json"


def _load_templates() -> dict:
    if TEMPLATES_PATH.exists():
        with open(TEMPLATES_PATH, encoding="utf-8") as f:
            return json.load(f).get("reasoning_templates", {})
    return {}


REASONING_TEMPLATES = _load_templates()


def _identify_legal_issues_with_templates(text: str, cause: str) -> list:
    """识别涉及的法律问题（含模板补充）"""
    issues = _identify_legal_issues(text, cause)
    for key, tmpl in REASONING_TEMPLATES.items():
        if key in cause or cause in key:
            for dispute in tmpl.get("common_disputes", [])[:3]:
                if dispute not in issues:
                    issues.append(dispute)
            break
    return issues[:8]


# ─── 主解析函数 ────────────────────────────────────────
def parse_case_elements(text: str, cause_hint: str = "") -> CaseElements:
    """
    从自然语言案情描述中提取结构化要素。
    优先使用增强解析器(LLM),失败降级为正则。
    """
    try:
        from enhanced_parser import parse_case_elements as enhanced_parse
        enhanced = enhanced_parse(text, cause_hint)
        return CaseElements(
            cause=enhanced.cause,
            parties=enhanced.parties,
            claims=enhanced.claims,
            facts=enhanced.facts,
            disputes=enhanced.disputes,
            evidence=enhanced.evidence,
            legal_issues=enhanced.legal_issues,
            applicable_laws=enhanced.applicable_laws,
            raw_text=enhanced.raw_text,
        )
    except ImportError:
        pass

    # fallback: 正则解析
    elements = CaseElements(raw_text=text)
    if cause_hint:
        elements.cause = cause_hint
    else:
        elements.cause = _detect_cause(text)
    elements.parties = _extract_parties(text)
    elements.claims = _extract_claims(text)
    elements.facts = _extract_facts(text)
    elements.disputes = _extract_disputes(text)
    elements.evidence = _extract_evidence(text)
    elements.legal_issues = _identify_legal_issues_with_templates(text, elements.cause)
    elements.applicable_laws = _get_applicable_laws(elements.cause)
    return elements
