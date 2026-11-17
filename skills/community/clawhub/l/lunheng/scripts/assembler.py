"""
pipeline/assembler.py — 三段论组装模块
从 pipeline.py 拆分而来 (2026-07-18)
职责：检索结果 → 判决书草稿 (JudgmentDraft)
"""

import json
import os
import re
import sys
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from error_utils import retry_with_backoff, log_error, log_warning, log_info

# ─── 路径 ───────────────────────────────────────────────
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data" / "shape_spirit"
REFS_DIR = SKILL_DIR / "refs"

# ─── Ref 文档加载 ──────────────────────────────────────
def _load_ref(name: str) -> str:
    ref_path = REFS_DIR / name
    if ref_path.exists():
        return ref_path.read_text(encoding="utf-8")
    return ""


PROCEDURAL_KNOWLEDGE = _load_ref("procedural_knowledge.md")

# ─── 说理模板 ──────────────────────────────────────────
TEMPLATES_PATH = DATA_DIR / "reasoning_templates.json"


def _load_templates() -> dict:
    if TEMPLATES_PATH.exists():
        with open(TEMPLATES_PATH, encoding="utf-8") as f:
            return json.load(f).get("reasoning_templates", {})
    return {}


REASONING_TEMPLATES = _load_templates()


# ─── LLM 配置（从统一配置模块导入）───────────────
from config import LLM_API_KEY as _LLM_KEY, LLM_BASE_URL as _LLM_URL, LLM_MODEL as _LLM_MODEL


# ─── 数据结构 ──────────────────────────────────────────
@dataclass
class JudgmentDraft:
    """判决书草稿"""
    case_info: dict = field(default_factory=dict)
    parties_section: str = ""
    cause_of_action: str = ""
    claims_section: str = ""
    facts_section: str = ""
    evidence_section: str = ""
    reasoning_section: str = ""
    verdict_section: str = ""
    footer_section: str = ""
    retrieved_cases: list = field(default_factory=list)
    retrieved_laws: list = field(default_factory=list)
    retrieved_patterns: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


# ─── 费用计算 ──────────────────────────────────────────
try:
    from fee_calculator import calculate_fee
except ImportError:
    def calculate_fee(case_type='财产', amount=0, **kw): return None


# ─── 各部分构建函数 ────────────────────────────────────
def _build_parties_section(elements) -> str:
    lines = []
    for role in ["原告", "被告", "第三人"]:
        names = elements.parties.get(role, [])
        if names:
            for name in names:
                # 添加更详细的当事人信息
                if role == "原告":
                    lines.append(f"原告：{name}，女，19XX年X月X日出生，汉族，住XX省XX市XX区XX路XX号。")
                elif role == "被告":
                    lines.append(f"被告：{name}，男，19XX年X月X日出生，汉族，住XX省XX市XX区XX路XX号。")
                else:
                    lines.append(f"第三人：{name}")
    return "\n".join(lines) if lines else "(当事人信息待补充)"


def _build_claims_section(elements) -> str:
    if not elements.claims:
        return "(诉讼请求待补充--请提供起诉状或明确诉讼请求)"
    lines = ["原告向本院提出诉讼请求:"]
    for i, claim in enumerate(elements.claims, 1):
        clean = re.sub(r'^\d+[.、))]\s*', '', claim)
        clean = re.sub(r'^请求(?:判令|判决|被告|原告)', '', clean)
        clean = clean.strip().rstrip('。;;')
        if clean:
            lines.append(f"{i}、{clean}。")
    return "\n".join(lines)


def _build_facts_section(elements) -> str:
    lines = []
    if elements.facts:
        lines.append("经审理查明:")
        for i, fact in enumerate(elements.facts, 1):
            fact = fact.strip().rstrip('。;;')
            lines.append(f"({i}){fact}。")
    else:
        lines.append("(事实认定部分待补充--请提供更详细的案情描述)")
    return "\n\n".join(lines)


def _build_evidence_section(elements, retrieval: dict) -> str:
    lines = []
    if elements.evidence:
        lines.append("以上事实,有以下证据证明:")
        for i, ev in enumerate(elements.evidence, 1):
            lines.append(f"{i}、{ev}。")
    else:
        lines.append("以上事实,有当事人陈述、书证等证据证明。")
    return "\n".join(lines)


def _build_footer_section() -> str:
    import random
    import datetime
    
    # 生成随机案号
    year = datetime.datetime.now().year
    case_num = random.randint(1000, 9999)
    
    lines = [
        "审判长　　×××",
        "审判员　　×××",
        "人民陪审员　×××",
        "",
        f"二〇二四年×月×日",
        "",
        "书记员　　×××",
    ]
    return "\n".join(lines)


def _extract_amount_from_claims(claims: list) -> float:
    max_amount = 0.0
    for claim in claims:
        for m in re.finditer(r'(\d[\d,.]*)\s*万?元', claim):
            try:
                val = float(m.group(1).replace(',', ''))
                if '万' in claim[max(0, m.start()-5):m.end()+5]:
                    val *= 10000
                max_amount = max(max_amount, val)
            except ValueError:
                pass
    return max_amount


def _calc_fee_line(elements) -> str:
    amount = _extract_amount_from_claims(elements.claims)
    cause = elements.cause
    if any(kw in cause for kw in ["离婚", "婚姻"]):
        case_type = "离婚"
    elif any(kw in cause for kw in ["人格权", "名誉", "肖像", "姓名", "隐私"]):
        case_type = "人格权"
    elif any(kw in cause for kw in ["著作权", "专利", "商标", "知识产权"]):
        case_type = "知识产权"
    elif any(kw in cause for kw in ["劳动", "工伤", "经济补偿"]):
        case_type = "劳动争议"
    elif any(kw in cause for kw in ["行政"]):
        case_type = "行政"
    else:
        case_type = "财产"
    try:
        result = calculate_fee(case_type, amount)
        if result and result.reduced_fee > 0:
            return f"案件受理费{result.reduced_fee:,}元,由被告负担。"
    except Exception:
        pass
    return "案件受理费由被告负担。"


def _build_verdict_section(elements) -> str:
    lines = ["判决如下:", ""]
    if elements.claims:
        for i, claim in enumerate(elements.claims, 1):
            clean = re.sub(r'^\d+[.、))]\s*', '', claim)
            lines.append(f"{i}、{clean};")
    else:
        lines.append("(判决主文待补充)")
    lines.append("")
    lines.append("如果未按本判决指定的期间履行给付金钱义务,应当依照《中华人民共和国民事诉讼法》第二百六十四条之规定,加倍支付迟延履行期间的债务利息。")
    lines.append("")
    lines.append(_calc_fee_line(elements))
    lines.append("")
    lines.append("如不服本判决,可以在判决书送达之日起十五日内向本院递交上诉状,并按对方当事人的人数提出副本,上诉于××××中级人民法院。")
    return "\n".join(lines)


def _generate_warnings(elements, retrieval: dict) -> list:
    warnings = []
    if not elements.facts:
        warnings.append("⚠️ 案情描述中未提取到关键事实,请补充详细案情")
    if not elements.disputes:
        warnings.append("⚠️ 未识别到明确争议焦点,建议明确双方分歧点")
    if not elements.claims:
        warnings.append("⚠️ 未提取到诉讼请求,请提供起诉状或明确请求事项")
    if not retrieval.get("入库案例"):
        warnings.append("⚠️ 未检索到入库案例,需确认是否为新类型案件")
    if not retrieval.get("法律法规") and not elements.applicable_laws:
        warnings.append("⚠️ 未检索到相关法条,请确认法律依据")
    if elements.cause == "民事纠纷":
        warnings.append("⚠️ 案由未明确识别,建议指定具体案由")
    if not retrieval.get("优秀文书"):
        warnings.append("i️ 未找到同类优秀文书范式参考")
    return warnings


# ─── LLM 生成 ──────────────────────────────────────────
def _llm_generate_judgment(elements, retrieval):
    """用 LLM 基于检索材料生成高质量判决书"""
    if not _LLM_KEY:
        return None

    cases_ctx = ""
    for i, r in enumerate(retrieval.get("入库案例", [])[:3], 1):
        cases_ctx += "\n案例{}: {}\n{}\n".format(i, r.title, r.content[:300])

    laws_ctx = ""
    for i, r in enumerate(retrieval.get("法律法规", [])[:3], 1):
        laws_ctx += "\n法条{}: {}\n{}\n".format(i, r.title, r.content[:200])

    patterns_ctx = ""
    for i, r in enumerate(retrieval.get("优秀文书", [])[:2], 1):
        tips = r.metadata.get("writing_experience", "") or r.content[:300]
        patterns_ctx += "\n范式{}: {}\n{}\n".format(i, r.title, tips)

    refs_ctx = ""
    for ref_key in ("参考文档", "领域知识"):
        for r in retrieval.get(ref_key, []):
            if r.content and len(r.content.strip()) > 50:
                refs_ctx += "\n" + r.content[:2000] + "\n"

    procedural_ctx = ""
    if PROCEDURAL_KNOWLEDGE:
        relevant_sections = []
        cause_short = elements.cause[:4]
        for section in PROCEDURAL_KNOWLEDGE.split("## "):
            if any(kw in section for kw in [cause_short, "三段论", "证据链", "减法原则", "对抗性思维"]):
                relevant_sections.append("## " + section[:600])
        procedural_ctx = "\n".join(relevant_sections[:2])

    template = {}
    for key in REASONING_TEMPLATES:
        if key in elements.cause or elements.cause in key:
            template = REASONING_TEMPLATES[key]
            break
    template_ctx = ""
    if template:
        template_ctx = "\n说理结构: {}\n审查要点: {}\n常见争议: {}".format(
            template.get("structure", ""),
            ", ".join(template.get("key_points", [])),
            ", ".join(template.get("common_disputes", [])))

    parties_str = ""
    for role in ["原告", "被告", "第三人"]:
        for n in elements.parties.get(role, []):
            parties_str += "{}: {}\n".format(role, n)

    prompt_sections = [
        "你是一位资深法官,擅长撰写高质量裁判文书。请根据以下材料撰写一份民事判决书。",
        "",
        "## 案件信息",
        f"案由: {elements.cause}",
        "当事人:",
        parties_str,
        f"诉讼请求: {', '.join(elements.claims[:5])}",
        f"关键事实: {', '.join(elements.facts[:8])}",
        f"争议焦点: {', '.join(elements.disputes[:4])}",
        f"法律问题: {', '.join(elements.legal_issues[:4])}",
        f"适用法条: {', '.join(elements.applicable_laws[:4])}",
        f"证据: {', '.join(elements.evidence[:5])}",
    ]

    if cases_ctx.strip():
        prompt_sections += ["", "## 参考入库案例", cases_ctx]
    if laws_ctx.strip():
        prompt_sections += ["", "## 相关法律法规", laws_ctx]
    if patterns_ctx.strip():
        prompt_sections += ["", "## 优秀文书写作范式", patterns_ctx]
    if template_ctx.strip():
        prompt_sections += ["", "## 说理模板", template_ctx]
    if procedural_ctx.strip():
        prompt_sections += ["", "## 资深法官思维指南", procedural_ctx]
    if refs_ctx.strip():
        prompt_sections += ["", "## 知识库参考文档", refs_ctx]

    prompt_sections += [
        "", "## 要求",
        "严格按照以下格式撰写,每个部分必须充实、专业：",
        "",
        "### 当事人",
        "（列出原告、被告信息）",
        "",
        "### 诉讼请求",
        "（逐项列出原告的诉讼请求）",
        "",
        "### 事实认定",
        "经审理查明：",
        "（详细叙述案件事实,按时间线组织,包含时间、金额、行为等关键要素）",
        "",
        "### 证据",
        "（列明支持事实认定的证据）",
        "",
        "### 本院认为",
        "（这是最核心的部分,必须做到：",
        "1.先归纳争议焦点",
        "2.逐一分析每个争议焦点,结合法条和类案进行说理",
        "3.引用具体法条（如《民法典》第XXX条）",
        "4.参考入库案例的裁判要点",
        "5.运用三段论逻辑: 大前提(法律)→小前提(事实)→结论",
        "6.说理要充分、有深度）",
        "",
        "### 判决如下",
        "（根据说理结论,逐项列出判决主文）",
        "",
        "只输出判决书正文,不要输出其他说明。",
        "",
        "⚠️ 引用规则（必须遵守）：",
        "- 禁止凭空构造法条：引用的法律条款必须来自上方「相关法律法规」列表",
        "- 禁止虚构裁判案号：引用的类案必须来自上方「参考入库案例」列表",
        "- 未找到对应法条时：在说理中注明「适用相关法律规定」，而非虚构具体条款",
        "- 确认引用的法律版本为现行有效版本（注意民法典已替代旧法）",
    ]

    prompt = "\n".join(prompt_sections)

    body = json.dumps({
        "model": _LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 4000,
    }).encode("utf-8")

    try:
        print("  LLM 生成判决书...", file=sys.stderr)
        req = urllib.request.Request(
            f"{_LLM_URL}/chat/completions", data=body,
            headers={"Authorization": f"Bearer {_LLM_KEY}", "Content-Type": "application/json"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=120)
        text = json.loads(resp.read())["choices"][0]["message"]["content"]

        draft = JudgmentDraft()
        draft.case_info = {"案由": elements.cause, "当事人": elements.parties}
        draft.cause_of_action = elements.cause

        sections = _parse_llm_judgment(text)
        
        # 当事人部分：始终使用模板（LLM 生成的当事人部分经常是废话）
        draft.parties_section = _build_parties_section(elements)
        draft.claims_section = sections.get("诉讼请求", _build_claims_section(elements))
        draft.facts_section = sections.get("事实认定", _build_facts_section(elements))
        draft.evidence_section = sections.get("证据", _build_evidence_section(elements, retrieval))
        draft.reasoning_section = sections.get("本院认为", "")
        draft.verdict_section = sections.get("判决如下", "")
        draft.footer_section = _build_footer_section()

        draft.retrieved_cases = [{"title": r.title, "content": r.content[:300]} for r in retrieval.get("入库案例", []) if r.title]
        draft.retrieved_laws = [{"title": r.title, "content": r.content[:300]} for r in retrieval.get("法律法规", []) if r.title]
        draft.retrieved_patterns = [{"title": r.title, "content": r.content[:300], "metadata": r.metadata} for r in retrieval.get("优秀文书", []) if r.title]
        draft.warnings = _generate_warnings(elements, retrieval)

        print(f"  LLM 生成完成: {len(text)} 字符", file=sys.stderr)
        return draft

    except urllib.error.HTTPError as e:
        if e.code == 429:
            log_warning("assembler", "_llm_generate_judgment", "429 限流，降级为模板组装")
        else:
            log_error("assembler", "_llm_generate_judgment", e, {"http_code": e.code})
        return None
    except Exception as e:
        log_error("assembler", "_llm_generate_judgment", e)
        print(f"  LLM 生成失败: {e}, 降级为模板组装", file=sys.stderr)
        return None


def _parse_llm_judgment(text):
    """解析 LLM 生成的判决书为各部分"""
    sections = {}
    markers = ["当事人", "诉讼请求", "事实认定", "经审理查明", "证据", "本院认为", "判决如下"]
    positions = []
    for m in markers:
        idx = text.find(m)
        if idx >= 0:
            positions.append((idx, m))
    positions.sort()

    for i, (pos, marker) in enumerate(positions):
        end = positions[i+1][0] if i+1 < len(positions) else len(text)
        content = text[pos:end].strip()
        for mk in markers:
            if content.startswith(mk):
                content = content[len(mk):].lstrip(": 、\n")
                break
        if marker in ("经审理查明", "事实认定"):
            sections["事实认定"] = content
        else:
            sections[marker] = content
    return sections


# ─── 模板组装 (LLM 降级方案) ──────────────────────────
def _build_reasoning_section(elements, retrieval: dict) -> str:
    """构建本院认为部分(三段论推理)"""
    sections = []

    template = {}
    for key in REASONING_TEMPLATES:
        if key in elements.cause or elements.cause in key:
            template = REASONING_TEMPLATES[key]
            break

    template_structure = template.get("structure", "")
    template_points = template.get("key_points", [])
    template_tips = template.get("sample_writing_tips", [])

    all_disputes = list(elements.disputes)
    if not all_disputes:
        template_disputes = template.get("common_disputes", [])
        all_disputes = [f"本案{d}如何认定" for d in template_disputes[:3]]

    if all_disputes:
        sections.append("本院认为:")
        sections.append("")
        sections.append(f"本案的争议焦点为:{'; '.join(all_disputes[:4])}。")
        sections.append("")
    else:
        sections.append("本院认为:")
        sections.append("")

    sections.append("关于法律适用问题。")

    seen_laws = set()
    all_law_texts = []

    def _law_key(law: str) -> str:
        m = re.match(r'(.+?第[\d\-条]+)', law)
        return m.group(1) if m else law

    template_laws = template.get("applicable_laws", [])
    for law in elements.applicable_laws + template_laws:
        key = _law_key(law)
        if key not in seen_laws:
            seen_laws.add(key)
            all_law_texts.append(law)

    for r in retrieval.get("法律法规", [])[:3]:
        title = r.title
        if title and len(title) < 60:
            key = _law_key(title)
            if key not in seen_laws and not re.search(r'丛书|大全|释评|释论|适用大全', title):
                seen_laws.add(key)
                all_law_texts.append(title)

    if all_law_texts:
        sections.append(f"根据{('、'.join(all_law_texts[:3]))},")

    if template_structure:
        sections.append(f"关于{elements.cause}案件,应当审查{template_structure}。")
    sections.append("")

    sections.append("关于事实认定问题。")
    sections.append("")

    if elements.facts:
        for fact in elements.facts[:6]:
            fact = fact.strip().rstrip('。;;')
            sections.append(f"{fact}。")
    else:
        sections.append("(事实认定部分待补充)")
    sections.append("")

    if template_points:
        sections.append("关于法律适用的具体分析。")
        sections.append("")
        for i, point in enumerate(template_points[:5], 1):
            sections.append(f"{i}、{point}。")
        sections.append("")

    case_refs = retrieval.get("入库案例", [])
    if case_refs:
        sections.append("参照类案裁判要点。")
        for r in case_refs[:2]:
            if r.content and len(r.content) > 20:
                content = r.content[:250].strip()
                sections.append(f"如{r.title[:30]}案中,{content}。")
        sections.append("")

    pattern_refs = retrieval.get("优秀文书", [])
    if pattern_refs and template_tips:
        sections.append("关于说理方式。")
        for tip in template_tips[:2]:
            sections.append(tip)
        sections.append("")

    sections.append("综上所述,")
    if elements.claims:
        sections.append("原告的诉讼请求合法有据,本院予以支持。")
    else:
        sections.append("原告的诉讼请求部分成立,本院予以支持。")

    return "\n".join(sections)


def _inject_disclaimer(draft):
    """在判决书末尾注入 AI 辅助生成免责声明（Task 4.2）"""
    disclaimer = (
        "\n【说明】"
        "本文书由 AI 辅助生成（论衡 Lunheng），仅供辅助参考。"
        "请办案人员/律师在正式使用前核对案件事实与现行生效法条。"
    )
    if hasattr(draft, 'verdict_section') and draft.verdict_section:
        draft.verdict_section += disclaimer
    if hasattr(draft, 'reasoning_section') and draft.reasoning_section:
        # 附加结构化溯源元数据
        draft.reasoning_section += (
            "\n\n【引用来源】"
            "法律依据及类案信息详见检索报告，点击条款编号可查看原始出处。"
        )


# ─── 主组装函数 ────────────────────────────────────────
def assemble_judgment(elements, retrieval: dict) -> JudgmentDraft:
    """
    基于检索结果,组装判决书草稿。
    优先使用 LLM 生成(高质量),失败降级为模板组装。
    """
    # 输入验证
    if not elements or not hasattr(elements, 'cause'):
        log_warning("assembler", "assemble_judgment", "要素对象为空或无效，使用默认值")
        from parser import CaseElements
        elements = CaseElements(raw_text="(输入为空)")
    if not retrieval:
        retrieval = {}

    llm_draft = _llm_generate_judgment(elements, retrieval)
    if llm_draft:
        return llm_draft

    draft = JudgmentDraft()
    draft.case_info = {"案由": elements.cause, "当事人": elements.parties}
    draft.cause_of_action = elements.cause

    draft.parties_section = _build_parties_section(elements)
    draft.claims_section = _build_claims_section(elements)
    draft.facts_section = _build_facts_section(elements)
    draft.evidence_section = _build_evidence_section(elements, retrieval)
    draft.reasoning_section = _build_reasoning_section(elements, retrieval)
    draft.verdict_section = _build_verdict_section(elements)
    draft.footer_section = _build_footer_section()

    draft.retrieved_cases = [
        {"title": r.title, "content": r.content[:300]}
        for r in retrieval.get("入库案例", []) if r.title
    ]
    draft.retrieved_laws = [
        {"title": r.title, "content": r.content[:300]}
        for r in retrieval.get("法律法规", []) if r.title
    ]
    draft.retrieved_patterns = [
        {"title": r.title, "content": r.content[:300], "metadata": r.metadata}
        for r in retrieval.get("优秀文书", []) if r.title
    ]

    draft.warnings = _generate_warnings(elements, retrieval)
    
    # 追加免责声明（Task 4.2）
    _inject_disclaimer(draft)
    
    return draft
