#!/usr/bin/env python3
"""
增强版案情要素解析器 (LLM + Regex 混合模式)
- 优先使用 LLM 提取结构化要素（准确率 ~90%+）
- LLM 失败时降级为正则解析（准确率 ~70%）
"""

import json
import os
import re
import sys
import urllib.request
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# ─── API 配置（从统一配置模块导入）───────────────
from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL


# ─── 数据结构 ──────────────────────────────────────────
@dataclass
class CaseElements:
    """从案情描述中解析出的结构化要素"""
    cause: str = ''                    # 案由
    parties: dict = field(default_factory=dict)  # 当事人 {原告:[], 被告:[], 第三人:[]}
    claims: list = field(default_factory=list)    # 诉讼请求
    facts: list = field(default_factory=list)     # 关键事实
    disputes: list = field(default_factory=list)  # 争议焦点
    evidence: list = field(default_factory=list)  # 关键证据
    legal_issues: list = field(default_factory=list)  # 涉及法律问题
    applicable_laws: list = field(default_factory=list)  # 适用法条
    raw_text: str = ''                 # 原始输入
    parse_method: str = ''             # 解析方法: llm / regex / hybrid


# ─── LLM 解析 ──────────────────────────────────────────
SYSTEM_PROMPT = """你是一位资深法官助理，擅长从案情描述中提取结构化法律要素。

请从用户提供的案情描述中提取以下要素，输出严格的 JSON 格式：

{
  "cause": "案由（如：民间借贷纠纷、买卖合同纠纷等）",
  "parties": {
    "原告": ["原告姓名/名称列表"],
    "被告": ["被告姓名/名称列表"],
    "第三人": ["第三人姓名/名称列表（如有）"]
  },
  "claims": ["诉讼请求1", "诉讼请求2", "..."],
  "facts": ["关键事实1", "关键事实2", "..."],
  "disputes": ["争议焦点1", "争议焦点2", "..."],
  "evidence": ["证据1", "证据2", "..."],
  "legal_issues": ["法律问题1", "法律问题2", "..."],
  "applicable_laws": ["适用法条1（如：民法典第667条）", "适用法条2", "..."]
}

提取规则：
1. 案由：根据案件性质准确识别，参考最高法《民事案件案由规定》
2. 当事人：提取自然人姓名或法人名称，区分原告/被告/第三人
3. 诉讼请求：提取原告的具体请求事项（金额、行为等）
4. 关键事实：提取与案件相关的时间、地点、行为、金额等核心事实
5. 争议焦点：识别原被告之间的核心分歧点
6. 证据：提取文中提到的证据类型和内容
7. 法律问题：识别涉及的法律争议点（如合同效力、违约责任等）
8. 适用法条：根据案由和法律问题，列出应适用的具体法条

注意事项：
- 只输出 JSON，不要输出其他内容
- 如果某个字段信息不足，返回空数组 []
- 法条引用格式：法律名称+条款号，如"民法典第667条"
- 案由必须是规范案由，不能用笼统的"民事纠纷"
"""


def llm_parse_elements(text: str, cause_hint: str = '') -> Optional[CaseElements]:
    """使用 LLM 解析案情要素"""
    if not LLM_API_KEY:
        print("  ⚠️ LLM API key 未配置，跳过 LLM 解析", file=sys.stderr)
        return None

    user_msg = text
    if cause_hint:
        user_msg = f"案由提示：{cause_hint}\n\n案情描述：\n{text}"

    body = json.dumps({
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        "temperature": 0.1,
        "max_tokens": 2000,
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

    try:
        print("  🤖 调用 LLM 解析要素...", file=sys.stderr)
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read())
        content = data["choices"][0]["message"]["content"]

        # 提取 JSON（可能被 markdown 包裹）
        json_match = re.search(r'\{[\s\S]*\}', content)
        if not json_match:
            print("  ⚠️ LLM 返回内容中未找到 JSON", file=sys.stderr)
            return None

        parsed = json.loads(json_match.group())

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
            parse_method="llm",
        )

        # 验证基本字段
        if not elements.cause:
            print("  ⚠️ LLM 未识别案由", file=sys.stderr)
            return None

        print(f"  ✅ LLM 解析成功: 案由={elements.cause}, "
              f"当事人={sum(len(v) for v in elements.parties.values())}人, "
              f"事实={len(elements.facts)}条, "
              f"争议={len(elements.disputes)}个", file=sys.stderr)

        return elements

    except Exception as e:
        print(f"  ⚠️ LLM 调用失败: {e}", file=sys.stderr)
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


def regex_parse_elements(text: str, cause_hint: str = '') -> CaseElements:
    """使用正则表达式解析案情要素（fallback）"""
    elements = CaseElements(raw_text=text, parse_method='regex')

    # 1. 案由
    if cause_hint:
        elements.cause = cause_hint
    else:
        elements.cause = _detect_cause(text)

    # 2. 当事人
    elements.parties = _extract_parties(text)

    # 3. 诉讼请求
    elements.claims = _extract_claims(text)

    # 4. 关键事实
    elements.facts = _extract_facts(text)

    # 5. 争议焦点
    elements.disputes = _extract_disputes(text)

    # 6. 证据
    elements.evidence = _extract_evidence(text)

    # 7. 法律问题
    elements.legal_issues = _identify_legal_issues(text, elements.cause)

    # 8. 适用法条
    elements.applicable_laws = _get_applicable_laws(elements.cause)

    return elements


def _detect_cause(text):
    scores = {}
    for cause, keywords in CAUSE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[cause] = score
    return max(scores, key=scores.get) if scores else '民事纠纷'


def _extract_parties(text):
    """提取当事人信息（支持自然人 + 法人/公司）"""
    parties = {"原告": [], "被告": [], "第三人": []}
    # 公司/法人名称模式（后缀后可跟分/支行等）
    _CORP = r'[\u4e00-\u9fa5（）()\d]{2,40}(?:有限公司|股份有限公司|集团|银行|医院|学校|基金会|协会|合作社|事务所)[\u4e00-\u9fa5]*'
    _PERSON = r'[\u4e00-\u9fa5]{2,6}'
    _NAME = f'(?:{_CORP}|{_PERSON})'
    for role in ["原告", "被告", "第三人"]:
        patterns = [
            rf'{role}[：:]\s*({_NAME})',
            rf'{role}({_NAME})(?:与|诉|和)',
            rf'{role}({_NAME})(?:系|为|向)',
            # 案由/一案边界
            rf'{role}({_NAME})(?:一案|纠纷|民间借贷|买卖合同|租赁合同|离婚|交通事故|侵权|劳动争议|继承)',
            # 顿号分隔（多个当事人）
            rf'{role}({_NAME})、',
            # 句号/逗号边界
            rf'{role}({_NAME})[。；，]',
        ]
        for pat in patterns:
            matches = re.findall(pat, text)
            for m in matches:
                name = m.strip()
                name = re.split(r'民间借贷|纠纷|一案|合同|买卖|租赁|侵权|诉讼|刑事|民事|离婚|交通事故|劳动争议|继承|不当得利|保证合同|物业服务|公司决议|医疗损害|建设工程', name)[0]
                if len(name) < 2:
                    continue
                is_corp = bool(re.search(r'公司|集团|银行|医院|学校|基金会|协会|合作社|事务所', name))
                max_len = 40 if is_corp else 6
                if len(name) > max_len or name in parties[role]:
                    continue
                if not is_corp:
                    if re.search(r'系|为|向|朋友|与|诉|和|但|而|于|因|在|的|一案|纠纷|以|根据|驾驶|骑|发生|负|构成|误将|操作|损害|知情', name):
                        continue
                    if not re.match(r'^[\u4e00-\u9fa5]+$', name):
                        continue
                    if re.match(r'^[以根据在从对向把被]', name):
                        continue
                parties[role].append(name)
    # 后处理：提取顿号分隔的多个当事人
    for role in ["原告", "被告", "第三人"]:
        if not parties[role]:
            continue
        for existing_name in list(parties[role]):
            esc = re.escape(existing_name)
            cont_pat = rf'{esc}[、，]({_NAME})'
            for m in re.finditer(cont_pat, text):
                extra = m.group(1).strip()
                extra = re.split(r'民间借贷|纠纷|一案|合同|买卖|租赁|侵权|诉讼|刑事|民事', extra)[0]
                if extra not in parties[role] and len(extra) >= 2:
                    is_corp = bool(re.search(r'公司|集团|银行|医院|学校', extra))
                    if is_corp or (re.match(r'^[\u4e00-\u9fa5]+$', extra) and len(extra) <= 6):
                        parties[role].append(extra)
    return parties


def _extract_claims(text):
    claims = []
    match = re.search(r'诉讼请求[：:\s]*(.+?)(?=(?:事实|理由|此致|此上|证据|$))', text, re.DOTALL)
    if match:
        items = re.split(r'\n\s*\d+[.、）)]\s*', match.group(1))
        claims = [item.strip() for item in items if item.strip() and len(item.strip()) > 3]
    if not claims:
        raw = re.findall(r'请求[^。]*?(?:判令|判决|支持)[^。]+', text)
        for r in raw:
            body = re.sub(r'^请求[^：:]*[：:]?\s*', '', r)
            items = re.split(r'\d+[.、）)]\s*', body)
            for item in items:
                item = item.strip().rstrip('；;，, ')
                if item and len(item) > 3:
                    claims.append(item)
    return claims[:10]


def _extract_facts(text):
    facts = []
    exclude_pat = re.compile(r'(?:诉讼请求|请求判令|请求支付|请求被告|本案诉讼|判令|判决|原告认为|被告认为|被告辩称|被告偿|被告支付|原告请求)')
    for pattern in [
        r'(?:经审理查明|本院认定|经查明|案件事实|查明)[：:\s]*(.+?)(?=(?:本院认为|判决如下|综上|以上事实|证据|原告主张|被告抗辩|$))',
        r'(?:事实与理由)[：:\s]*(.+?)(?=(?:本院认为|判决如下|综上|$))',
        r'(?:事情经过|事情经过如下)[：:\s]*(.+?)(?=(?:原告|被告|综上|$))',
    ]:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            items = re.split(r'[。；\n]', match.group(1))
            facts = [item.strip() for item in items if item.strip() and len(item.strip()) > 8 and not exclude_pat.search(item)]
            break
    if not facts:
        sentences = re.split(r'[。；\n]', text)
        for s in sentences:
            s = s.strip()
            if len(s) < 10 or exclude_pat.search(s):
                continue
            if re.search(r'\d{4}年|万元|元|借|还|签|付|交|约定|到期|违约|死亡|受伤|事故|转账|偿还', s):
                facts.append(s)
    return facts[:15]


def _extract_disputes(text):
    disputes = []
    match = re.search(r'(?:争议焦点|争点|焦点问题|双方争议)[：:\s]*(.+?)(?=(?:本院认为|事实|判决|综上|$))', text, re.DOTALL)
    if match:
        items = re.split(r'\n\s*\d+[.、）)]\s*', match.group(1))
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


def _extract_evidence(text):
    evidence = []
    match = re.search(r'(?:证据|证据清单|主要证据)[：:\s]*(.+?)(?=(?:事实|理由|本院认为|判决|$))', text, re.DOTALL)
    if match:
        items = re.split(r'\n\s*\d+[.、）)]\s*', match.group(1))
        evidence = [item.strip() for item in items if item.strip() and len(item.strip()) > 5]
    return evidence[:10]


def _identify_legal_issues(text, cause):
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
    "确认合同效力": {"laws": ["民法典第144-157条"], "primary": "合同效力"},
    "医疗损害": {"laws": ["民法典第1218-1228条", "医疗纠纷预防和处理条例"], "primary": "医疗损害责任"},
    "保险合同": {"laws": ["保险法"], "primary": "保险合同"},
    "不当得利": {"laws": ["民法典第985-988条"], "primary": "不当得利"},
    "保证合同": {"laws": ["民法典第681-702条"], "primary": "保证合同"},
}


def _get_applicable_laws(cause):
    for key, info in CAUSE_LAW_MAP.items():
        if key in cause:
            return info["laws"]
    for key, info in CAUSE_LAW_MAP.items():
        if any(kw in cause for kw in [key, info["primary"]]):
            return info["laws"]
    return ["民法典"]


# ─── 混合解析（主入口） ────────────────────────────────
def parse_case_elements(text: str, cause_hint: str = '') -> CaseElements:
    """
    混合解析：LLM 优先，失败降级为正则。

    Returns:
        CaseElements (parse_method 字段标明使用了哪种方法)
    """
    # 1. 尝试 LLM 解析
    llm_result = llm_parse_elements(text, cause_hint)
    if llm_result:
        return llm_result

    # 2. 降级为正则解析
    print("  📝 降级为正则解析...", file=sys.stderr)
    return regex_parse_elements(text, cause_hint)


# ─── CLI ───────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description='增强版案情要素解析器')
    parser.add_argument('--input', '-i', help='案情描述文本')
    parser.add_argument('--file', '-f', help='案情描述文件路径')
    parser.add_argument('--cause', '-c', help='案由提示')
    parser.add_argument('--json', action='store_true', help='JSON 输出')
    parser.add_argument('--regex-only', action='store_true', help='仅使用正则解析')
    args = parser.parse_args()

    text = ''
    if args.input:
        text = args.input
    elif args.file:
        text = Path(args.file).read_text(encoding='utf-8')
    else:
        print('请提供案情描述：--input 或 --file')
        return

    if args.regex_only:
        result = regex_parse_elements(text, args.cause or '')
    else:
        result = parse_case_elements(text, args.cause or '')

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print(f'案由: {result.cause}')
        print(f'解析方法: {result.parse_method}')
        print(f'当事人: {result.parties}')
        print(f'诉讼请求 ({len(result.claims)}): {result.claims[:3]}')
        print(f'关键事实 ({len(result.facts)}): {result.facts[:3]}')
        print(f'争议焦点 ({len(result.disputes)}): {result.disputes[:3]}')
        print(f'证据 ({len(result.evidence)}): {result.evidence[:3]}')
        print(f'法律问题: {result.legal_issues}')
        print(f'适用法条: {result.applicable_laws}')


if __name__ == '__main__':
    main()
