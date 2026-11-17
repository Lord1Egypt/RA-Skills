#!/usr/bin/env python3
"""
法条引用校验模块（三层验证架构）
Layer 1: 本地快查 — 20部核心法律 + 7部司法解释
Layer 2: LLM 校验 — 任意法律引用，通用无需维护
Layer 3: IMA 知识库（可选）
"""

import json
import os
import re
import sys
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from rapidfuzz import fuzz, process

# ─── Layer 1: 本地核心法律库 ──────────────────────────
LOCAL_LAWS = {
    # ═══ 民事实体法 ═══
    "中华人民共和国民法典": {"short": "民法典", "articles": 1260, "replaces": ["合同法", "物权法", "侵权责任法", "担保法", "婚姻法", "继承法", "民法通则", "民法总则"]},
    "中华人民共和国公司法": {"short": "公司法", "articles": 266},
    "中华人民共和国合伙企业法": {"short": "合伙企业法", "articles": 109},
    "中华人民共和国企业破产法": {"short": "企业破产法", "articles": 136},
    "中华人民共和国票据法": {"short": "票据法", "articles": 115},
    "中华人民共和国保险法": {"short": "保险法", "articles": 121},
    "中华人民共和国海商法": {"short": "海商法", "articles": 278},
    "中华人民共和国消费者权益保护法": {"short": "消费者权益保护法", "articles": 63},
    "中华人民共和国产品质量法": {"short": "产品质量法", "articles": 74},
    "中华人民共和国反不正当竞争法": {"short": "反不正当竞争法", "articles": 37},
    "中华人民共和国电子商务法": {"short": "电子商务法", "articles": 89},
    "中华人民共和国旅游法": {"short": "旅游法", "articles": 112},
    "中华人民共和国民用航空法": {"short": "民用航空法", "articles": 215},
    "中华人民共和国铁路法": {"short": "铁路法", "articles": 73},
    "中华人民共和国公路法": {"short": "公路法", "articles": 87},
    # ═══ 知识产权法 ═══
    "中华人民共和国商标法": {"short": "商标法", "articles": 73},
    "中华人民共和国专利法": {"short": "专利法", "articles": 76},
    "中华人民共和国著作权法": {"short": "著作权法", "articles": 67},
    "中华人民共和国反垄断法": {"short": "反垄断法", "articles": 63},
    # ═══ 劳动与社会保障法 ═══
    "中华人民共和国劳动合同法": {"short": "劳动合同法", "articles": 98},
    "中华人民共和国劳动法": {"short": "劳动法", "articles": 107},
    "中华人民共和国劳动合同法实施条例": {"short": "劳动合同法实施条例", "articles": 38},
    "中华人民共和国社会保险法": {"short": "社会保险法", "articles": 98},
    "中华人民共和国劳动争议调解仲裁法": {"short": "劳动争议调解仲裁法", "articles": 54},
    "中华人民共和国工伤保险条例": {"short": "工伤保险条例", "articles": 67},
    # ═══ 环境资源法 ═══
    "中华人民共和国环境保护法": {"short": "环境保护法", "articles": 70},
    "中华人民共和国水污染防治法": {"short": "水污染防治法", "articles": 103},
    "中华人民共和国大气污染防治法": {"short": "大气污染防治法", "articles": 129},
    "中华人民共和国土壤污染防治法": {"short": "土壤污染防治法", "articles": 99},
    "中华人民共和国固体废物污染环境防治法": {"short": "固废污染防治法", "articles": 130},
    "中华人民共和国环境影响评价法": {"short": "环境影响评价法", "articles": 49},
    # ═══ 行政法 ═══
    "中华人民共和国行政处罚法": {"short": "行政处罚法", "articles": 86},
    "中华人民共和国行政诉讼法": {"short": "行政诉讼法", "articles": 103},
    "中华人民共和国行政复议法": {"short": "行政复议法", "articles": 90},
    "中华人民共和国行政许可法": {"short": "行政许可法", "articles": 83},
    "中华人民共和国行政强制法": {"short": "行政强制法", "articles": 72},
    "中华人民共和国国家赔偿法": {"short": "国家赔偿法", "articles": 42},
    "中华人民共和国政府信息公开条例": {"short": "政府信息公开条例", "articles": 56},
    # ═══ 民事程序法 ═══
    "中华人民共和国民事诉讼法": {"short": "民事诉讼法", "articles": 291},
    "中华人民共和国仲裁法": {"short": "仲裁法", "articles": 80},
    "中华人民共和国人民调解法": {"short": "人民调解法", "articles": 44},
    "中华人民共和国公证法": {"short": "公证法", "articles": 47},
    # ═══ 刑事法 ═══
    "中华人民共和国刑法": {"short": "刑法", "articles": 452},
    "中华人民共和国刑事诉讼法": {"short": "刑事诉讼法", "articles": 308},
    # ═══ 其他常用 ═══
    "中华人民共和国城乡规划法": {"short": "城乡规划法", "articles": 72},
    "中华人民共和国建筑法": {"short": "建筑法", "articles": 85},
    "中华人民共和国土地管理法": {"short": "土地管理法", "articles": 86},
    "中华人民共和国城市房地产管理法": {"short": "城市房地产管理法", "articles": 73},
    "中华人民共和国道路交通安全法": {"short": "道路交通安全法", "articles": 124},
    "中华人民共和国食品安全法": {"short": "食品安全法", "articles": 155},
    "中华人民共和国义务教育法": {"short": "义务教育法", "articles": 63},
    "中华人民共和国个人信息保护法": {"short": "个人信息保护法", "articles": 74},
    "中华人民共和国数据安全法": {"short": "数据安全法", "articles": 55},
    "中华人民共和国网络安全法": {"short": "网络安全法", "articles": 79},
}

LOCAL_JUDICIAL = {
    # ═══ 民事类 ═══
    "最高人民法院关于审理民间借贷案件适用法律若干问题的规定": {"short": "民间借贷规定", "articles": 33},
    "最高人民法院关于适用《中华人民共和国民法典》合同编通则若干问题的解释": {"short": "合同编解释", "articles": 69},
    "最高人民法院关于审理建设工程施工合同纠纷案件适用法律问题的解释（一）": {"short": "建设工程司法解释", "articles": 45},
    "最高人民法院关于审理人身损害赔偿案件适用法律若干问题的解释": {"short": "人身损害赔偿解释", "articles": 24},
    "最高人民法院关于确定民事侵权精神损害赔偿责任若干问题的解释": {"short": "精神损害赔偿解释", "articles": 23},
    "最高人民法院关于审理道路交通事故损害赔偿案件适用法律若干问题的解释": {"short": "交通事故赔偿解释", "articles": 25},
    "最高人民法院关于适用《中华人民共和国民法典》婚姻家庭编的解释（一）": {"short": "婚姻家庭编解释", "articles": 91},
    "最高人民法院关于适用《中华人民共和国民法典》继承编的解释（一）": {"short": "继承编解释", "articles": 38},
    "最高人民法院关于适用《中华人民共和国民法典》物权编的解释（一）": {"short": "物权编解释", "articles": 22},
    "最高人民法院关于审理买卖合同纠纷案件适用法律问题的解释": {"short": "买卖合同解释", "articles": 41},
    "最高人民法院关于审理融资租赁合同纠纷案件适用法律问题的解释": {"short": "融资租赁解释", "articles": 20},
    "最高人民法院关于审理劳动争议案件适用法律问题的解释（一）": {"short": "劳动争议解释", "articles": 72},
    # ═══ 执行类 ═══
    "最高人民法院关于民事执行中变更、追加当事人若干问题的规定": {"short": "变更追加当事人规定", "articles": 35},
    "最高人民法院关于人民法院民事执行中查封、扣押、冻结财产的规定": {"short": "查封扣押冻结规定", "articles": 32},
    "最高人民法院关于人民法院民事执行中拍卖、变卖财产的规定": {"short": "拍卖变卖规定", "articles": 36},
    # ═══ 行政类 ═══
    "最高人民法院关于适用《中华人民共和国行政诉讼法》的解释": {"short": "行政诉讼法解释", "articles": 163},
}

REPEALED = {
    "合同法": "已废止，由《民法典》合同编替代（2021-01-01起）",
    "物权法": "已废止，由《民法典》物权编替代",
    "侵权责任法": "已废止，由《民法典》侵权责任编替代",
    "担保法": "已废止，由《民法典》担保制度替代",
    "婚姻法": "已废止，由《民法典》婚姻家庭编替代",
    "继承法": "已废止，由《民法典》继承编替代",
    "民法通则": "已废止，由《民法典》总则编替代",
    "民法总则": "已废止，由《民法典》总则编替代",
    "公司法（2018修正）": "已废止，由2024年新《公司法》替代",
}

# ─── Layer 2: LLM 配置（从统一配置模块导入）───────
from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
XIAOMI_API_KEY = LLM_API_KEY
XIAOMI_BASE_URL = LLM_BASE_URL

# ─── Layer 3: 国家法律法规数据库 API ─────────────────
try:
    from npc_law_api import verify_law as npc_verify
    HAS_NPC_API = True
except ImportError:
    HAS_NPC_API = False
    def npc_verify(name): return {}

# ─── Layer 3.8: 法条智能路由 (Phase 2.2) ─────────────
try:
    from law_router import suggest_laws, resolve_law_alias, format_suggestions
    HAS_LAW_ROUTER = True
except ImportError:
    HAS_LAW_ROUTER = False
    def suggest_laws(*a, **kw): return []
    def resolve_law_alias(n): return n
    def format_suggestions(s): return ""

# ─── Layer 3.5: 国家行政法规库 (司法部) ───────────────
try:
    from moj_law_api import verify_law as moj_verify
    HAS_MOJ_API = True
except ImportError:
    HAS_MOJ_API = False
    def moj_verify(name): return {}

# 行政法规名称特征词（条例/规定/办法/规则/细则）
_ADMIN_REG_PATTERNS = re.compile(r'(?:条例|规定|办法|规则|细则|决定|命令)$')

# ─── 中文数字转换 ──────────────────────────────────────
_CN_MAP = {'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,
           '十':10,'百':100,'千':1000,'万':10000}

def _cn_to_arabic(cn):
    if not cn or re.match(r'^\d', cn):
        return cn
    result = temp = 0
    for c in cn:
        if c in _CN_MAP:
            val = _CN_MAP[c]
            if val >= 10:
                result += (temp or 1) * val
                temp = 0
            else:
                temp = val
        else:
            return cn
    return str(result + temp) if (result + temp) > 0 else cn

# ─── 数据结构 ──────────────────────────────────────────
@dataclass
class LawRef:
    raw_text: str
    law_name: str = ""
    article_num: str = ""
    is_valid: bool = False
    source: str = ""
    warnings: list = field(default_factory=list)

@dataclass
class LawCheckResult:
    total_refs: int = 0
    valid_refs: int = 0
    warnings: list = field(default_factory=list)
    details: list = field(default_factory=list)
    missing_laws: list = field(default_factory=list)
    score: float = 0.0

# ─── 提取法条引用 ──────────────────────────────────────
def extract_law_refs(text):
    refs, seen = [], set()
    _CN = r'[零一二三四五六七八九十百千]+'
    _AR = r'[\d\-—]+'

    for pat, gname, gart in [
        # Pattern 1: 《法律名称》第X条 — 直接匹配
        (r'《([^》]+)》第(' + _CN + '|' + _AR + r')条', 1, 2),
        # Pattern 2: 根据/依照/依据《法律名称》第X条 — 书名号后直接跟条款
        (r'(?:根据|依照|依据|按照|参照|适用|符合|违反)《([^》]+)》第(' + _CN + '|' + _AR + r')条', 1, 2),
        # Pattern 3: 《法律名称》（版本标注）第X条 — 如《民间借贷规定》（2020年第二次修正）第二十五条
        (r'《([^》]+)》（[^）]*?修正[^）]*?）第(' + _CN + '|' + _AR + r')条', 1, 2),
        # Pattern 4: 法律名称简称第X条 — 无书名号，2-50个汉字（覆盖司法解释等长名称）
        (r'([\u4e00-\u9fa5]{2,50})第(' + _CN + '|' + _AR + r')条', 1, 2),
    ]:
        for m in re.finditer(pat, text):
            raw = m.group(0)
            if raw in seen:
                continue
            seen.add(raw)
            name = m.group(gname).strip() if gname and m.group(gname) else ""
            if not name:
                name = m.group(1).strip() if m.lastindex >= 1 and m.group(1) else ""
            art = m.group(gart)
            if re.match(r'^[\u4e00-\u9fa5]+$', art):
                art = _cn_to_arabic(art)
            # skip non-law names
            if re.match(r'^本院|^该院|^法院', name):
                continue
            refs.append(LawRef(raw_text=raw, law_name=name, article_num=art))
    return refs

# ─── Layer 1: 本地快查 ────────────────────────────────
def _fuzzy_match_law(name, candidates, threshold=80):
    """用 rapidfuzz 做模糊匹配，处理判决书中的法律名称简称/错字"""
    # 先尝试 token_sort_ratio（对乱序容忍度高）
    best_match = process.extractOne(
        name, candidates,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=threshold
    )
    if best_match:
        return best_match[0], best_match[1]
    # 降级到 partial_ratio（子串匹配）
    best_match = process.extractOne(
        name, candidates,
        scorer=fuzz.partial_ratio,
        score_cutoff=threshold + 5  # 提高阈值避免误匹配
    )
    if best_match:
        return best_match[0], best_match[1]
    return None, 0


def _local_validate(ref):
    name = ref.law_name.strip()
    # 收集所有候选名称（全称 + 简称）用于模糊匹配
    all_law_names = {}  # display_name -> full_name
    for full, info in LOCAL_LAWS.items():
        all_law_names[full] = full
        all_law_names[info["short"]] = full
    for full, info in LOCAL_JUDICIAL.items():
        all_law_names[full] = full
        all_law_names[info["short"]] = full

    # Phase 2.2: 先通过别名词典解析
    resolved = resolve_law_alias(name)
    if resolved != name:
        ref.warnings.append(f"别名解析：「{name}」→「{resolved}」")
        # 废止法别名：直接标记为废止，不走后续匹配
        if resolved.startswith("[已废止]"):
            ref.is_valid = False
            ref.source = "local"
            ref.warnings.append(f"已废止：{resolved}")
            return True
        name = resolved
        ref.law_name = name
    
    # 先检查现行法律（精确 + 子串，简称长度>=4防止误匹配）
    for full, info in LOCAL_LAWS.items():
        matched = False
        if name == full or name == info["short"]:
            matched = True
        elif info["short"] in name and len(info["short"]) >= 4 and len(name) - len(info["short"]) <= 6:
            matched = True
        if matched:
            ref.law_name = full
            ref.is_valid = True
            ref.source = "local"
            _check_article_range(ref, info)
            return True
    for full, info in LOCAL_JUDICIAL.items():
        matched = False
        if name == full or name == info["short"]:
            matched = True
        elif info["short"] in name and len(info["short"]) >= 4 and len(name) - len(info["short"]) <= 6:
            matched = True
        if matched:
            ref.law_name = full
            ref.is_valid = True
            ref.source = "local"
            _check_article_range(ref, info)
            return True

    # 先检查废止法律（必须在模糊匹配之前，避免"合同法"→"劳动合同法"的误匹配）
    for repealed, reason in REPEALED.items():
        if name == repealed or name == f"中华人民共和国{repealed}":
            ref.is_valid = False
            ref.source = "local"
            ref.warnings.append(f"已废止：{reason}")
            return True

    # 模糊匹配（处理判决书中的简称/错字，如"民法通"→"民法典"）
    if len(name) >= 3:
        fuzzy_name, fuzzy_score = _fuzzy_match_law(name, list(all_law_names.keys()))
        if fuzzy_name and fuzzy_score >= 85:
            full = all_law_names[fuzzy_name]
            ref.law_name = full
            ref.is_valid = True
            ref.source = "local_fuzzy"
            ref.warnings.append(f"模糊匹配：「{name}」≈「{fuzzy_name}」(相似度{fuzzy_score}%)")
            info = LOCAL_LAWS.get(full) or LOCAL_JUDICIAL.get(full)
            if info:
                _check_article_range(ref, info)
            return True
    return False


def _check_article_range(ref, info):
    """校验条款号是否合理（不超过最大条数，且不为 0）"""
    max_art = info.get("articles")
    if not max_art or not ref.article_num:
        return
    try:
        art_num = int(ref.article_num)
        if art_num <= 0:
            ref.is_valid = False
            ref.warnings.append(f"条款号无效：第{ref.article_num}条不存在")
        elif art_num > max_art:
            ref.is_valid = False
            ref.warnings.append(f"条款号越界：{ref.law_name}共{max_art}条，引用第{art_num}条不存在")
    except ValueError:
        pass

# ─── Layer 2: LLM 校验 ────────────────────────────────
def _llm_validate_batch(refs):
    if not XIAOMI_API_KEY or not refs:
        return refs
    ref_list = "\n".join(f"{i+1}. {r.law_name}第{r.article_num}条" for i, r in enumerate(refs))
    prompt = f"""你是中国法律专家。请校验以下法条引用是否正确。
规则：法律名称是否现行有效、条款号是否在范围内、错误则给出正确写法。
引用列表：
{ref_list}
输出 JSON 数组：[{{"index": 序号, "valid": true/false, "correct_name": "正确名称", "warning": "问题说明"}}]
只输出 JSON。"""

    body = json.dumps({"model": LLM_MODEL, "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.1, "max_tokens": 1500}).encode()
    try:
        req = urllib.request.Request(f"{XIAOMI_BASE_URL}/chat/completions", data=body,
            headers={"Authorization": f"Bearer {XIAOMI_API_KEY}", "Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=30)
        content = json.loads(resp.read())["choices"][0]["message"]["content"]
        match = re.search(r'\[[\s\S]*\]', content)
        if match:
            for r in json.loads(match.group()):
                idx = r.get("index", 0) - 1
                if 0 <= idx < len(refs):
                    refs[idx].is_valid = r.get("valid", False)
                    refs[idx].source = "llm"
                    if r.get("warning"):
                        refs[idx].warnings.append(r["warning"])
                    if r.get("correct_name"):
                        refs[idx].law_name = r["correct_name"]
    except Exception as e:
        print(f"  LLM 校验失败: {e}", file=sys.stderr)
    return refs

# ─── 主函数 ────────────────────────────────────────────
def check_law_references(text, cause=""):
    result = LawCheckResult()
    refs = extract_law_refs(text)
    result.total_refs = len(refs)
    if not refs:
        result.score = 50
        result.warnings.append("未检测到法条引用，建议在本院认为部分明确引用法律依据")
        return result

    local_known, llm_unknown = [], []
    for ref in refs:
        (local_known if _local_validate(ref) else llm_unknown).append(ref)

    # Layer 3.5: 行政法规库快速验证（对未识别的引用，若名称像行政法规则先查 MOJ）
    if HAS_MOJ_API and llm_unknown:
        moj_candidates = [r for r in llm_unknown if _ADMIN_REG_PATTERNS.search(r.law_name)]
        if moj_candidates:
            print(f"  行政法规库验证 {len(moj_candidates)} 条...", file=sys.stderr)
            for ref in moj_candidates:
                try:
                    moj_result = moj_verify(ref.law_name)
                    if moj_result.get("found"):
                        ref.is_valid = True
                        ref.source = "moj_api"
                        official = moj_result.get("title", "")
                        if official and official != ref.law_name:
                            ref.warnings.append(f"行政法规库确认名称：{official}")
                        # 从 llm_unknown 移到 local_known
                        llm_unknown.remove(ref)
                        local_known.append(ref)
                except Exception:
                    pass

    if llm_unknown:
        print(f"  LLM 校验 {len(llm_unknown)} 条未知引用...", file=sys.stderr)
        _llm_validate_batch(llm_unknown)

    # Layer 3: NPC API 权威验证（对 LLM 校验通过的做二次确认）
    if HAS_NPC_API:
        llm_validated = [r for r in llm_unknown if r.is_valid]
        if llm_validated:
            print(f"  NPC API 权威验证 {len(llm_validated)} 条...", file=sys.stderr)
            for ref in llm_validated:
                try:
                    npc_result = npc_verify(ref.law_name)
                    if npc_result.get("found"):
                        npc_status = npc_result.get("status_code", 0)
                        official = npc_result.get("official_name", "")
                        if npc_status == 1:  # 已废止
                            ref.is_valid = False
                            ref.source = "npc_api"
                            ref.warnings.append(f"NPC数据库确认已废止：{official}")
                        elif npc_status == 3:  # 有效
                            ref.source = "npc_api"  # 权威确认
                            if official and official != ref.law_name:
                                ref.law_name = official
                        elif npc_status == 2:  # 已修改
                            ref.source = "npc_api"
                            ref.warnings.append(f"NPC数据库确认已修改：{official}")
                except Exception:
                    pass  # NPC API 失败不影响结果

    all_refs = local_known + llm_unknown
    result.details = all_refs
    result.valid_refs = sum(1 for r in all_refs if r.is_valid)
    for r in all_refs:
        result.warnings.extend(r.warnings)

    for repealed, reason in REPEALED.items():
        if repealed in text:
            result.warnings.append(f"文书引用了已废止法律「{repealed}」：{reason}")

    if cause:
        result.missing_laws = _suggest_missing_laws(text, cause)
        # Phase 2.2: 法条智能路由建议
        if HAS_LAW_ROUTER:
            disputes = []
            legal_issues = []
            # 尝试从文本中提取争议焦点
            for pat in [r'争议焦点[：:](.+?)(?:\n|$)', r'本院认为(.+?)(?:\n|$)']:
                m = re.search(pat, text)
                if m:
                    disputes.append(m.group(1)[:100])
            route_suggestions = suggest_laws(cause, disputes, legal_issues)
            if route_suggestions:
                result.warnings.append(f"智能路由建议: {format_suggestions(route_suggestions)}")

    if result.total_refs > 0:
        base = (result.valid_refs / result.total_refs) * 80
        penalty = min(len(result.warnings) * 5, 30)
        result.score = max(0, min(100, base - penalty + 20))
    return result


def _suggest_missing_laws(text, cause):
    essential = {
        "民间借贷": [("民法典", "第667-680条", "借款合同"), ("民间借贷规定", "第2条", "起诉条件")],
        "买卖合同": [("民法典", "第595-646条", "买卖合同")],
        "劳动合同": [("劳动合同法", "第47条", "经济补偿"), ("劳动合同法", "第87条", "违法解除赔偿金")],
        "离婚纠纷": [("民法典", "第1079条", "准予离婚")],
        "交通事故": [("道路交通安全法", "第76条", "事故赔偿"), ("民法典", "第1179条", "人身损害赔偿范围")],
        "建设工程": [("民法典", "第788-808条", "建设工程合同")],
        "物业服务": [("民法典", "第937-950条", "物业服务合同")],
        "不当得利": [("民法典", "第985-988条", "不当得利")],
        "保证合同": [("民法典", "第681-702条", "保证合同")],
        "医疗损害": [("民法典", "第1218-1228条", "医疗损害责任")],
    }
    suggestions = []
    for key, laws in essential.items():
        if key in cause or cause in key:
            for law_short, articles, desc in laws:
                if law_short not in text and articles not in text:
                    suggestions.append(f"建议引用「{law_short}」{articles}（{desc}）")
            break
    return suggestions


def main():
    import argparse
    p = argparse.ArgumentParser(description="法条引用校验（三层验证）")
    p.add_argument("--input", "-i")
    p.add_argument("--file", "-f")
    p.add_argument("--cause", "-c", default="")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    text = args.input or (Path(args.file).read_text(encoding="utf-8") if args.file else "")
    if not text:
        print("请提供文书文本"); return

    result = check_law_references(text, args.cause)
    if args.json:
        print(json.dumps({"total": result.total_refs, "valid": result.valid_refs,
            "score": result.score, "warnings": result.warnings,
            "details": [{"raw": d.raw_text, "law": d.law_name, "article": d.article_num,
                         "valid": d.is_valid, "source": d.source} for d in result.details]
        }, ensure_ascii=False, indent=2))
    else:
        print(f"引用: {result.valid_refs}/{result.total_refs} | 得分: {result.score:.0f}")
        for d in result.details:
            print(f"  [{'V' if d.is_valid else 'X'}] [{d.source}] {d.raw_text}")

if __name__ == "__main__":
    main()
