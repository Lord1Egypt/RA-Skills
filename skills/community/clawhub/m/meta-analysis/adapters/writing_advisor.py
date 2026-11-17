# -*- coding: utf-8 -*-
"""
adapters/writing_advisor.py — 论文撰写与发表建议引擎（P2a 本地基线 + P2b 网络增强 + P2c 打磨）

消费 run_analysis 已生成的 res["_interpretation"] 与 res["_quality_advice"]，
基于 stats + 领域模板生成结构化发表建议（IMRaD 模板 / 限制段 / 讨论段 / 审稿人问题 /
目标期刊推荐 / PRISMA 清单 / 数据可用性）。

设计原则（见 论文撰写辅助_实施方案.md v2）：
  - P2a：纯本地。期刊推荐用 field_templates.json 静态种子，参考核验做结构层，离线可交付。
  - P2b：use_network=True 时查 OpenAlex sources 真实期刊指标 + verify_citations 真实参考核验
         （接线在 P2b；本文件保留网络层接口占位 _fetch_openalex_journals / _verify_refs_online，
          并由 run_analysis 注入；P2a 默认走静态/结构层，网络失败自动降级，不阻断主流程）。
  - P2c：use_network=True 时 ① 领域自动归类增强（用户 topic → 语料 meta.topic/concepts →
         OpenAlex works concepts，field_source 透明标注）；② 报告规范（PRISMA 2020 / MOOSE）
         权威出处 DOI 在线核验（prisma_source）；③ Semantic Scholar 高引推荐（有 key 才用）。
         三者均失败降级，不阻断主流程。
  - 绝不重算 interpretation / quality_advice（直接吃已生成结果）。
  - 防御性 fallback：缺 stats / 缺 interpretation / 领域未知 → 不抛，给安全默认。
"""

import os
import re
import json
import sys
import urllib.parse

_HERE = os.path.dirname(os.path.abspath(__file__))
_FIELD_TEMPLATES_PATH = os.path.join(_HERE, "..", "references", "field_templates.json")

# ── ct-literature 复用（懒加载；缺失则网络层降级，不阻断主流程） ───────────────
# P2b 复用 ct-literature 的 http_utils（OpenAlex 礼貌池 + 指数退避）与 verify_citations
# （DOI/PMID/OpenAlex 三重核验 + 标题作者一致性，抑制幻觉引用）。两者均纯 stdlib，
# 经 ct-literature 根目录加入 sys.path 后以 `adapters` 包导入。模块级全局便于单测 mock。
_CT_HTTP = None    # http_utils 模块（或 None）
_CT_VERIFY = None  # verify_citations 模块（或 None）


def _ensure_ct_lit():
    """惰性导入 ct-literature 复用模块；返回 (http_utils, verify_citations) 或 (None, None)。"""
    global _CT_HTTP, _CT_VERIFY
    if _CT_HTTP is not None or _CT_VERIFY is not None:
        return _CT_HTTP, _CT_VERIFY
    try:
        ct_root = os.path.join(os.path.dirname(os.path.dirname(_HERE)), "ct-literature")
        if os.path.isdir(ct_root) and ct_root not in sys.path:
            sys.path.insert(0, ct_root)
        from adapters import http_utils as _h  # noqa: F401
        from adapters import verify_citations as _v  # noqa: F401
        _CT_HTTP, _CT_VERIFY = _h, _v
    except Exception:
        _CT_HTTP, _CT_VERIFY = None, None
    return _CT_HTTP, _CT_VERIFY

# ── 领域模板（懒加载，文件缺失不影响主流程） ──────────────────────────────────
_FIELD_TEMPLATES = {}


def _load_field_templates():
    global _FIELD_TEMPLATES
    try:
        with open(_FIELD_TEMPLATES_PATH, encoding="utf-8") as f:
            _FIELD_TEMPLATES = json.load(f)
    except Exception:  # noqa: BLE001 — 种子缺失时退化为空，走 general 兜底
        _FIELD_TEMPLATES = {}


_load_field_templates()

# 关键词 → 领域 映射（纯规则，确定性强，可单测；命中即返回，不调 LLM）
_FIELD_KEYWORDS = [
    ("oncology", ["癌", "肿瘤", "cancer", "tumor", "tumour", "egfr", "nsclc", "oncolog",
                  "化疗", "靶向", "免疫治", "lymphoma", "leukemia", "白血病", "淋巴瘤"]),
    ("cardiology", ["心", "冠脉", "房颤", "心血管", "cardio", "coronary", "atrial",
                    "arrhythm", "heart", "myocard", "心梗", "卒", "房颤", "heart failure", "hf"]),
    ("neurology", ["神经", "脑", "卒", "阿尔茨", "parkinson", "neurolog", "stroke",
                   "alzheimer", "epilep", "多发性硬化", "ms "]),
    ("psychiatry", ["抑郁", "焦虑", "精神", "psychiat", "depress", "anxiet", "schizophr",
                    "bipolar", "双相"]),
    ("infectious_disease", ["感染", "病毒", "细菌", "infect", "hiv", "tb", "covid",
                            "antibiotic", "耐药", "vaccin", "疫苗"]),
    ("endocrinology", ["内分泌", "糖尿", "甲状腺", "endo", "diabet", "thyroid", "insulin",
                       "obesity", "肥胖"]),
    ("respiratory", ["呼吸", "肺", "哮喘", "copd", "respir", "asthma", "pulmon", "lung"]),
    ("gastroenterology", ["胃肠", "肝", "消化", "gastro", "hepat", "ibd", "crohn",
                          "ulcer", "colitis", "liver"]),
    ("rheumatology", ["风湿", "关节", "rheumat", "arthrit", "lupus", "系统性红斑狼疮", "sle"]),
]


# ── 领域推断 ──────────────────────────────────────────────────────────────────
def infer_field(topic=""):
    """从研究主题推断领域；未命中 → 'general'。纯规则、确定性强。"""
    if not topic:
        return "general"
    t = str(topic).lower()
    for field, kws in _FIELD_KEYWORDS:
        for kw in kws:
            if kw.lower() in t:
                return field
    return "general"


# ── P2c：领域自动归类增强（语料 concepts / OpenAlex concepts） ────────────────────
def _load_merged_data(merged_json):
    """把 merged_json（dict 或文件路径）读成 dict；失败返回 None。"""
    if isinstance(merged_json, dict):
        return merged_json
    if isinstance(merged_json, str) and merged_json:
        try:
            with open(merged_json, encoding="utf-8") as f:
                d = json.load(f)
            return d if isinstance(d, dict) else None
        except Exception:  # noqa: BLE001
            return None
    return None


def _concept_names(items):
    """从 concepts/keywords 列表抽 display_name；兼容 str / {'display_name':..} 两种形态。"""
    out = []
    for it in (items or []):
        if isinstance(it, str):
            out.append(it)
        elif isinstance(it, dict):
            nm = it.get("display_name") or it.get("name")
            if nm:
                out.append(nm)
    return out


def _vote_field_from_concept_names(names):
    """按概念/关键词名对 _FIELD_KEYWORDS 投票，返回 (field, score)；(None, 0) 表示无信号。

    去噪：泛概念（Medicine / Biology / Internal medicine …）不命中任何领域关键词，天然不投票。
    """
    score = {}
    for nm in names:
        if not nm:
            continue
        s = str(nm).lower()
        for field, kws in _FIELD_KEYWORDS:
            if any(kw.lower() in s for kw in kws):
                score[field] = score.get(field, 0) + 1
                break  # 同一概念名对一个领域最多计 1 票
    if not score:
        return None, 0
    best = max(score.items(), key=lambda kv: kv[1])
    return best[0], best[1]


def _infer_field_from_corpus(merged_json):
    """[P2c] 从已检索语料推断领域：先 meta.topic 规则命中，再 works concepts/keywords 投票。

    返回 (field, source) 或 None；source ∈ {'corpus_topic','corpus_concepts'}。
    """
    data = _load_merged_data(merged_json)
    if not data:
        return None
    meta = data.get("meta") if isinstance(data.get("meta"), dict) else {}
    topic = (meta.get("topic") or "") if meta else ""
    if topic:
        f = infer_field(topic)
        if f != "general":
            return f, "corpus_topic"
    names = []
    for w in (data.get("works") or []):
        if not isinstance(w, dict):
            continue
        names.extend(_concept_names(w.get("concepts")))
        names.extend(_concept_names(w.get("keywords")))
    f, _score = _vote_field_from_concept_names(names)
    if f:
        return f, "corpus_concepts"
    return None


def _infer_field_from_openalex(topic):
    """[P2c] 规则/语料均未命中时，用 OpenAlex works 搜索取 concepts 投票定域；失败返回 None。"""
    if not topic:
        return None
    _http, _ = _ensure_ct_lit()
    if _http is None:
        return None
    try:
        try:
            key = _http.load_openalex_key()
        except Exception:
            key = None
        hdrs = _http.build_openalex_headers(api_key=key)
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode({
            "search": topic, "per-page": 5, "select": "id,concepts,keywords"})
        data = _http.get_json(url, headers=hdrs, timeout=20, max_retries=2)
    except Exception:  # noqa: BLE001 — 网络失败 → 调用方降级 general
        return None
    names = []
    for r in ((data.get("results") or []) if isinstance(data, dict) else []):
        if not isinstance(r, dict):
            continue
        names.extend(_concept_names(r.get("concepts")))
        names.extend(_concept_names(r.get("keywords")))
    f, _score = _vote_field_from_concept_names(names)
    return f


def _infer_field_ex(topic="", field="", merged_json=None, use_network=False):
    """[P2c] 增强版领域推断，返回 (field, field_source)。

    优先级：explicit（用户指定）→ rule（topic 关键词）→ corpus（语料 meta.topic/concepts）
            → openalex（在线 works concepts）→ default（general）。
    """
    if field:
        return field, "explicit"
    f = infer_field(topic)
    if f != "general":
        return f, "rule"
    if merged_json:
        got = _infer_field_from_corpus(merged_json)
        if got:
            return got
    if use_network and topic:
        fo = _infer_field_from_openalex(topic)
        if fo:
            return fo, "openalex"
    return "general", "default"


# ── stats 防御性抽取 ────────────────────────────────────────────────────────────
def _extract_stats(stats, params=None):
    """从 coze stats 抽取常用字段，兼容多种键名（pooled/tables 差异）。"""
    s = stats or {}
    pooled = s.get("pooled") or {}
    het = s.get("heterogeneity") or {}
    bias = s.get("bias") or {}

    def _num(*keys, default=None):
        for k in keys:
            v = s.get(k)
            if isinstance(v, (int, float)):
                return v
        return default

    i2 = het.get("I2")
    if not isinstance(i2, (int, float)):
        i2 = s.get("I2")
    egger_p = bias.get("egger_p")
    if not isinstance(egger_p, (int, float)):
        egger_p = s.get("egger_p")
    return {
        "k": s.get("k"),
        "sm": s.get("sm") or (params or {}).get("sm") or "",
        "est_exp": pooled.get("estimate_exp"),
        "est": pooled.get("estimate"),
        "ci_low": pooled.get("ci_lower") if pooled.get("ci_lower") is not None else pooled.get("lower"),
        "ci_high": pooled.get("ci_upper") if pooled.get("ci_upper") is not None else pooled.get("upper"),
        "i2": i2,
        "tau2": het.get("tau2") if "tau2" in het else s.get("tau2"),
        "egger_p": egger_p,
        "model": (params or {}).get("model") or "",
    }


# ── strengths / limitations ─────────────────────────────────────────────────────
def _strengths(sx, field):
    out = []
    k = sx.get("k")
    if isinstance(k, int) and k >= 10:
        out.append("纳入研究数量较多（k=%d），统计效能较好" % k)
    elif isinstance(k, int) and k >= 3:
        out.append("多中心证据合并（k=%d）" % k)
    i2 = sx.get("i2")
    if isinstance(i2, (int, float)) and i2 < 25:
        out.append("异质性低（I²=%.0f%%）" % i2)
    eg = sx.get("egger_p")
    if isinstance(eg, (int, float)) and eg >= 0.05:
        out.append("未检测到显著发表偏倚（Egger p=%.2f）" % eg)
    if not out:
        out.append("基于现有证据完成合并效应估计")
    return out


def _limitations(sx, field):
    out = []
    k = sx.get("k")
    if isinstance(k, int) and k < 5:
        out.append("纳入研究数较少（k=%d），结论外推需谨慎" % k)
    i2 = sx.get("i2")
    if isinstance(i2, (int, float)) and i2 >= 50:
        out.append("存在高异质性（I²=%.0f%%），需探索来源" % i2)
    elif isinstance(i2, (int, float)) and i2 >= 25:
        out.append("存在中等异质性（I²=%.0f%%）" % i2)
    eg = sx.get("egger_p")
    if isinstance(eg, (int, float)) and eg < 0.05:
        out.append("检测到潜在发表偏倚（Egger p=%.2f）" % eg)
    ft = _FIELD_TEMPLATES.get(field) or _FIELD_TEMPLATES.get("general", {})
    out.extend(ft.get("common_limitations", []))
    # 去重保序
    seen, res = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


# ── 讨论段模板（填空式） ─────────────────────────────────────────────────────────
def _discussion_template(sx, interp, task="", ref_sections=None):
    # 2026-09-14：网络 Meta（nma / nma_rank / cnma）没有"单一合并效应量"（sx.est 取自
    # pooled 标量，对向量型 pooled 为 None）→ 此处不得套用单一合并效应量的措辞；
    # 证据质量框架也应写 CINeMA 六域而非 GRADE。
    _network = task in ("nma", "nma_rank", "cnma")
    sm = (str(sx.get("sm") or "OR")).upper()
    est = sx.get("est_exp") if sx.get("est_exp") is not None else sx.get("est")
    ci = ""
    if sx.get("ci_low") is not None and sx.get("ci_high") is not None:
        ci = "%.2f–%.2f" % (sx["ci_low"], sx["ci_high"])
    concl = (interp.get("conclusion") or "") if isinstance(interp, dict) else ""
    parts = []
    if est is not None and not _network:
        parts.append("本研究发现合并效应量为 %s=%.2f（95%%CI %s）。" % (sm, est, ci))
        if sx.get("ci_low") is not None and sx["ci_low"] > 0:
            parts.append("合并效应量置信区间未跨 1，提示干预与结局显著相关，")
        else:
            parts.append("置信区间跨 1，未显示显著统计学意义，需谨慎解读；")
    if concl:
        parts.append(concl)
    parts.append(
        "然而，异质性来源、偏倚风险与证据质量（%s）仍需在讨论中充分说明，"
        "并对照下方「限制段要点」逐条回应。" % ("CINeMA 六域（网络置信度）" if _network else "GRADE")
    )

    # ref_sections：参考同类文献的讨论段写法（2026-09-17 新增）
    if ref_sections:
        ref_parts = []
        for key, info in list(ref_sections.items())[:3]:
            title = info.get("title", key)
            secs = info.get("sections", {})
            disc = secs.get("discussion", "")
            if disc:
                ref_parts.append(f"\n--- 参考 [{title}] 的讨论段 ---\n{disc[:1500]}")
            if len("\n".join(ref_parts)) > 4000:
                break
        if ref_parts:
            parts.append(
                "\n\n### 同类文献讨论段参考（仅作写作风格/结构借鉴，不可直接复制，"
                "也不可将其数据视为你的研究结果）：\n"
                + "\n".join(ref_parts)
            )

    return "".join(parts)


# ── 期刊推荐（P2a 静态；P2b 网络 hook） ──────────────────────────────────────────
def _recommend_journals(field, sx, use_network):
    """返回 (recs, source, metrics_source, network_ok, network_attempted)。

    P2a：仅静态种子。P2b：若 use_network 且 _fetch_openalex_journals 可用则查真实指标，
    失败回退静态（network_ok=False）。
    """
    ft = _FIELD_TEMPLATES.get(field) or _FIELD_TEMPLATES.get("general", {})
    tiers = ft.get("journal_tiers", [])
    recs = []
    for j in tiers[:5]:
        recs.append({
            "name": j.get("name"),
            "tier": j.get("tier"),
            "if": j.get("if"),
            "approx": j.get("approx", False),
            "why": j.get("why") or ("%s 档期刊，匹配本 meta 的证据量级与领域" % j.get("tier")),
            "metrics_source": "seed",
        })
    source = "static_seed"
    metrics_source = "seed"
    network_ok = None
    network_attempted = False

    # P2b 网络增强（默认开；复用 ct-literature.http_utils 查 OpenAlex sources）
    if use_network:
        network_attempted = True
        try:
            _openalex = _fetch_openalex_journals(field, sx)
            if _openalex:
                recs, metrics_source = _openalex
                source = "openalex"
                network_ok = True
            else:
                network_ok = False  # 已尝试但无网络结果（keyless/断网/ct-literature 缺失）
        except Exception:  # noqa: BLE001 — 网络失败静默降级静态
            network_ok = False
    return recs, source, metrics_source, network_ok, network_attempted


def _fetch_openalex_journals(field, sx):
    """[P2b] 查 OpenAlex sources 实时指标，覆盖静态种子。

    返回 (recs, "openalex") 或 None（ct-literature 不可用 / 网络失败 / 无种子 → 调用方降级静态）。
    优先 keyed 池（OPENALEX_API_KEY），无 key 走 keyless（100/day，足够单次建议）。
    """
    _http, _ = _ensure_ct_lit()
    if _http is None:
        return None
    http_utils = _http
    ft = _FIELD_TEMPLATES.get(field) or _FIELD_TEMPLATES.get("general", {})
    tiers = ft.get("journal_tiers") or []
    if not tiers:
        return None
    key = None
    try:
        key = http_utils.load_openalex_key()
    except Exception:
        key = None
    hdrs = http_utils.build_openalex_headers(api_key=key)
    base = "https://api.openalex.org/sources"
    enhanced = []
    for j in tiers[:5]:
        name = j.get("name")
        rec = dict(j)
        if not name:
            enhanced.append(rec)
            continue
        try:
            url = "%s?search=%s&per_page=5" % (base, urllib.parse.quote(name))
            data = http_utils.get_json(url, headers=hdrs, timeout=20, max_retries=2)
            srcs = (data.get("results") or []) if isinstance(data, dict) else []
            hit = None
            nl = name.lower()
            for s in srcs:
                dn = (s.get("display_name") or "").lower()
                if dn and (nl in dn or dn in nl):
                    hit = s
                    break
            if hit is None and srcs:
                hit = srcs[0]
            if hit is None:
                enhanced.append(rec)
                continue
            ss = hit.get("summary_stats") or {}
            mc = ss.get("2yr_mean_citedness")
            if isinstance(mc, (int, float)):
                rec["if"] = round(float(mc), 1)
                rec["approx"] = False
                rec["if_proxy"] = True
            hidx = hit.get("h_index")
            if isinstance(hidx, (int, float)):
                rec["h_index"] = hidx
            cbc = hit.get("cited_by_count")
            if isinstance(cbc, (int, float)):
                rec["cited_by_count"] = cbc
            apc_list = hit.get("apc_prices") or []
            if apc_list and isinstance(apc_list, list):
                first = apc_list[0]
                if isinstance(first, dict):
                    cur = first.get("currency") or ""
                    price = first.get("price")
                    if isinstance(price, (int, float)):
                        rec["apc_prices"] = ("%s %.0f" % (cur, price)) if cur else ("%.0f" % price)
            oa = hit.get("is_oa")
            if isinstance(oa, bool):
                rec["is_oa"] = oa
            rec["metrics_source"] = "openalex"
            rec["openalex_id"] = hit.get("id")
            enhanced.append(rec)
        except Exception:  # noqa: BLE001 — 单刊失败保留静态种子，不阻断整批
            enhanced.append(rec)
            continue
    if not enhanced:
        return None
    return enhanced, "openalex"


# ── 审稿人问题 ───────────────────────────────────────────────────────────────────
def _reviewer_questions(field, interp, ref_sections=None):
    qs = []
    if isinstance(interp, dict):
        qs.extend(list(interp.get("reviewer_questions") or []))
    ft = _FIELD_TEMPLATES.get(field) or _FIELD_TEMPLATES.get("general", {})
    qs.extend(ft.get("reviewer_questions", []))
    qs.extend([
        "是否评估了纳入研究的偏倚风险（Cochrane RoB 2.0 / NOS）？",
        "是否探索了异质性来源（亚组分析 / meta 回归）？",
        "是否考虑了发表偏倚对结果的影响（Egger / Begg）？",
    ])
    # 参考同类文献审稿人可能追问的角度（2026-09-17 新增）
    if ref_sections:
        ref_disc = []
        for key, info in list(ref_sections.items())[:3]:
            secs = info.get("sections", {})
            disc = secs.get("discussion", "")
            if disc:
                ref_disc.append(disc)
        if ref_disc:
            qs.append(
                "参考同类文献讨论段的写法，本 meta 的分析结论是否需要进一步说明临床意义与应用场景？"
            )
    seen, res = set(), []
    for q in qs:
        if q not in seen:
            seen.add(q)
            res.append(q)
    return res


# ── 参考核验（P2a 结构层；P2b 真实在线） ─────────────────────────────────────────
_DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$", re.I)


def _verify_refs_structural(references):
    out = []
    for r in (references or []):
        if not isinstance(r, dict):
            continue
        doi = r.get("doi")
        if doi and _DOI_RE.search(str(doi).strip()):
            out.append({"doi": str(doi).strip(), "status": "format_ok", "via": "structural",
                        "note": "DOI 格式合法（未做在线核验；P2b 将接 verify_citations 真实解析）"})
        elif doi:
            out.append({"doi": str(doi), "status": "malformed", "via": "structural",
                        "note": "DOI 格式疑似异常，请人工核对"})
        else:
            out.append({"doi": (doi or ""), "status": "no_identifier", "via": "structural",
                        "note": "无 DOI，无法在线核验"})
    return out


def _verify_refs_online(references):
    """[P2b] 真实在线核验（verify_citations.verify_one）。

    ct-literature 不可用时抛 NotImplementedError → 调用方降级结构层。返回 dict 列表，
    形状与 _verify_refs_structural 对齐（doi/status/via/note），并增补 verified/consistency/title_ratio。
    status 词汇：verified / bot_blocked / mismatch / unresolved / no_identifier / suspicious。
    """
    _, _verify = _ensure_ct_lit()
    if _verify is None:
        raise NotImplementedError("ct-literature 不可用，无法在线核验")
    verify_citations = _verify
    out = []
    for r in (references or []):
        if not isinstance(r, dict):
            continue
        doi = r.get("doi")
        if not doi:
            out.append({"doi": "", "status": "no_identifier", "via": "online",
                        "note": "无 DOI，无法在线核验", "verified": False})
            continue
        doi = str(doi).strip()
        try:
            res = verify_citations.verify_one({"doi": doi}, timeout=15)
        except Exception:  # noqa: BLE001 — 单条异常退化为格式层校验，不阻断整批
            if _DOI_RE.search(doi):
                out.append({"doi": doi, "status": "format_ok", "via": "structural_fallback",
                            "note": "在线核验异常，已退化为格式层校验", "verified": None})
            else:
                out.append({"doi": doi, "status": "malformed", "via": "structural_fallback",
                            "note": "DOI 格式疑似异常", "verified": False})
            continue
        out.append({
            "doi": doi,
            "status": res.get("citation_verify_status", "unresolved"),
            "via": "online",
            "note": res.get("citation_verify_note", ""),
            "verified": res.get("citation_verified"),
            "consistency": res.get("citation_consistency"),
            "title_ratio": res.get("citation_title_ratio"),
        })
    return out


def _refs_from_merged(merged_json):
    """[P2b] 从 .merged.json 抽取带 DOI 的 works 作为待核验参考文献（最多前 10 条）。"""
    data = _load_merged_data(merged_json)
    if not isinstance(data, dict):
        return []
    works = data.get("works") or []
    out = []
    for w in works:
        if isinstance(w, dict) and w.get("doi"):
            out.append({"doi": w["doi"]})
        if len(out) >= 10:
            break
    return out


def _ground_evidence(merged_json, sx):
    """[P2b] 复用 .merged.json 做证据接地：报告真实检索语料规模并与 stats.k 对齐。"""
    res = {"loaded": False, "n_works": None, "k_match": None,
           "source": "merged.json", "note": ""}
    data = _load_merged_data(merged_json)
    if not isinstance(data, dict):
        if isinstance(merged_json, str) and merged_json:
            res["note"] = "merged.json 读取失败"
        return res
    res["loaded"] = True
    works = data.get("works") or []
    res["n_works"] = len(works)
    k = sx.get("k")
    if isinstance(k, int):
        res["k_match"] = (res["n_works"] == k)
        if res["k_match"]:
            res["note"] = ("证据已对齐检索语料（merged.json works=%d，与纳入研究数 k=%d 一致）。"
                           % (res["n_works"], k))
        else:
            res["note"] = ("检索语料 merged.json 含 %d 篇，与纳入分析 k=%d 不同（可能为去重/筛选后子集）。"
                           % (res["n_works"], k))
    else:
        res["note"] = "检索语料 merged.json 含 %d 篇（stats 未提供 k，无法对齐）。" % res["n_works"]
    return res


# ── PRISMA / 数据可用性 ─────────────────────────────────────────────────────────
def _prisma_checklist(task):
    # 2026-09-14：网络 Meta 的证据质量要求是 CINeMA 六域（不是普通 GRADE），
    # 且 cnma / nma_rank 与 nma 同属网络家族，此前只在 task == "nma" 时追加
    # 一致性检验项 → cnma / nma_rank 的清单缺项（加性假设 / 排序不确定性）。
    _network = task in ("nma", "nma_rank", "cnma")
    base = ["检索策略（含数据库与日期）", "筛选流程（PRISMA 流程图）", "偏倚风险评估",
            "CINeMA 证据置信度（六域）" if _network else "GRADE 证据质量",
            "效应量估计与置信区间"]
    if task in ("nma", "nma_rank"):
        base.append("网络一致性检验（node-splitting / 全局一致性）")
    if task == "cnma":
        base.append("网络一致性检验（design-by-treatment）+ 成分加性假设检验（Q.diff）")
    if task == "nma_rank":
        base.append("排序概率（SUCRA / P-score）及其不确定性说明")
    if task == "metareg":
        base.append("协变量说明与回归诊断")
    return base


# ── P2c：报告规范登记 + 权威出处在线核验 ─────────────────────────────────────────
# PRISMA/MOOSE 等规范的条目本身稳定（当前版为 PRISMA 2020），无需抓取易变页面；
# 联网时核验其「权威出处 DOI」是否真实解析，并附 EQUATOR 条目页，使清单可溯源、可引用。
_REPORTING_STANDARDS = {
    "prisma_2020": {
        "name": "PRISMA 2020",
        "doi": "10.1136/bmj.n71",
        "url": "https://www.equator-network.org/reporting-guidelines/prisma/",
    },
    "moose": {
        "name": "MOOSE",
        "doi": "10.1001/jama.283.15.2008",
        "url": "https://www.equator-network.org/reporting-guidelines/moose/",
    },
}


def _reporting_standards(task, use_network):
    """[P2c] 报告规范登记 + 在线核验其出处 DOI。

    返回 (standards, prisma_source)：
      standards = [{key,name,doi,url,status,note}]；status 静态时为 'static'，联网核验后为验证词表状态。
      prisma_source = 'verified_online'（至少一条出处核验通过）| 'static'（未联网 / 降级）。
    """
    keys = ["prisma_2020"]
    if task in ("pairwise_meta", "nma", "metareg"):
        keys.append("moose")
    standards = []
    for k in keys:
        st = _REPORTING_STANDARDS.get(k)
        if not st:
            continue
        standards.append({"key": k, "name": st["name"], "doi": st["doi"],
                          "url": st["url"], "status": "static", "note": "",
                          "resolved": None})
    prisma_source = "static"
    if use_network and standards:
        try:
            vres = _verify_refs_online([{"doi": s["doi"]} for s in standards])
            n_ok = 0
            for s, v in zip(standards, vres):
                s["status"] = v.get("status") or "unresolved"
                s["note"] = v.get("note") or ""
                # citation_verified=True 表示 DOI 已在 doi.org 解析到真实资源：
                # ok（200/206）与 bot_blocked（出版方 403，DOI 真实）均算已解析；
                # mismatch / unresolved 不算。
                s["resolved"] = bool(v.get("verified"))
                if s["resolved"]:
                    n_ok += 1
            if n_ok:
                prisma_source = "verified_online"
        except NotImplementedError:
            pass  # ct-literature 不可用 → 保留静态登记
        except Exception:  # noqa: BLE001 — 可选增强，失败不阻断
            pass
    return standards, prisma_source


# ── P2c：Semantic Scholar 高引推荐（有 key 才用） ────────────────────────────────
_S2_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"


def _highly_cited(topic, field, use_network, limit=5):
    """[P2c] Semantic Scholar 高引论文推荐。

    沿用 ct-literature 既有策略：无 key 时完全跳过（不发注定 429 的请求）。
    返回 (rows, status)：rows = [{title,year,citations,venue,doi}]；
    status ∈ ok | skipped_no_network | skipped_no_client | skipped_no_key | skipped_no_query | degraded。
    """
    if not use_network:
        return [], "skipped_no_network"
    _http, _ = _ensure_ct_lit()
    if _http is None:
        return [], "skipped_no_client"
    try:
        key = _http.load_s2_key()
    except Exception:
        key = None
    if not key:
        return [], "skipped_no_key"
    q = topic or field
    if not q:
        return [], "skipped_no_query"
    try:
        url = _S2_SEARCH + "?" + urllib.parse.urlencode({
            "query": q, "limit": 20,
            "fields": "title,year,citationCount,venue,externalIds"})
        data = _http.get_json(url, headers=_http.build_s2_headers(key),
                              timeout=30, max_retries=2)
    except Exception:  # noqa: BLE001 — 可选增强源，失败即降级
        return [], "degraded"
    rows = []
    for w in ((data.get("data") or []) if isinstance(data, dict) else []):
        if not isinstance(w, dict):
            continue
        ext = w.get("externalIds") or {}
        rows.append({"title": w.get("title") or "", "year": w.get("year"),
                     "citations": w.get("citationCount") or 0,
                     "venue": w.get("venue") or "", "doi": ext.get("DOI")})
    rows.sort(key=lambda r: -(r.get("citations") or 0))
    return rows[:limit], "ok"


def _data_availability():
    return "建议公开分析代码与数据（如 PROSPERO 注册、OSF / GitHub 托管），提升可重复性。"


# ── 主入口 ───────────────────────────────────────────────────────────────────────
def advise_publication(stats=None, task="pairwise_meta", params=None, topic="", field="",
                       grade="", grade_framework="", interpretation=None, references=None,
                       merged_json=None, use_network=True, ref_sections=None):
    """生成结构化发表建议。

    参数：
      stats:        coze 返回 stats（pooled/heterogeneity/bias/k/sm）
      task:         任务类型（pairwise_meta / nma / metareg / ...）
      params:       {sm, model, ...}
      topic:        研究主题（用户给或 query 推断）
      field:        领域；缺省由 infer_field(topic) 推断，未知→'general'
      grade:        证据质量等级（优先用 _quality_advice.grade.grade）
      grade_framework: 该等级所属框架 —— "GRADE" / "CINeMA"。
                    网络 Meta（nma / nma_rank / cnma）走 CINeMA 六域，其
                    grade 值是 major_concerns / some_concerns / ... 而非
                    High/Moderate/Low/VeryLow；带框架前缀可避免二者混读
                    （2026-09-14 修复：此前 grade_reported 只写裸值）。
      interpretation: 复用 _interpretation（conclusion/caveats/reviewer_questions）
      references:   用户参考文献列表（dict w/ doi）→ P2a 结构层 / P2b 在线核验
      merged_json:  已检索语料（路径或 dict；P2b 证据接地：报告语料规模 + 与 k 对齐；
                    无 references 时取其 DOI 用于在线核验）
      use_network:  False=纯本地（--no-network）；True 时启用 P2b/P2c 网络增强（失败自动降级）
      ref_sections: 已纳入 PDF 的章节切片（写作风格/结构参考），可选；
                    有值时 discussion_template 与 reviewer_questions 可参考同类文献写法
    """
    field_used, field_source = _infer_field_ex(topic, field, merged_json, use_network)
    interp = interpretation if isinstance(interpretation, dict) else {}
    sx = _extract_stats(stats, params)

    # P2b 证据接地：复用 .merged.json 报告真实检索语料规模
    evidence = _ground_evidence(merged_json, sx)
    # 未提供 references 但有 merged_json -> 取其 DOI 用于在线核验
    if not references and merged_json and use_network:
        _mj = _refs_from_merged(merged_json)
        if _mj:
            references = _mj

    strengths = _strengths(sx, field_used)
    limitations = _limitations(sx, field_used)
    # ref_sections 传给 discussion 模板和审稿人问题生成
    discussion = _discussion_template(sx, interp, task, ref_sections=ref_sections)
    reviewer_qs = _reviewer_questions(field_used, interp, ref_sections=ref_sections)
    recs, source, metrics_source, network_ok, _attempted = _recommend_journals(field_used, sx, use_network)
    # P2c：报告规范出处核验 + Semantic Scholar 高引推荐（均为可选增强，失败降级）
    standards, prisma_source = _reporting_standards(task, use_network)
    highly_cited, s2_status = _highly_cited(topic, field_used, use_network)

    # 期刊推荐文案
    if recs:
        _top = "、".join("%s（%s）" % (r["name"], r["tier"]) for r in recs[:3])
        journal_fit = "建议投稿方向：%s。%s" % (_top, _FIELD_TEMPLATES.get(field_used, {}).get("reporting_guideline", ""))
    else:
        journal_fit = "未匹配到领域期刊种子，建议补充专科期刊检索后重试。"

    # 参考核验
    if references:
        if use_network:
            try:
                ref_verification = _verify_refs_online(references)
            except NotImplementedError:
                ref_verification = _verify_refs_structural(references)
        else:
            ref_verification = _verify_refs_structural(references)
    else:
        ref_verification = []

    return {
        "reporting_checklist": _FIELD_TEMPLATES.get(field_used, {}).get("reporting_guideline", "PRISMA 2020"),
        "strengths": strengths,
        "limitations": limitations,
        "discussion_template": discussion,
        "reviewer_likely_questions": reviewer_qs,
        "journal_fit": journal_fit,
        "prisma_checklist": _prisma_checklist(task),
        "data_availability": _data_availability(),
        "recommended_journals": recs,
        "ref_verification": ref_verification,
        "field_used": field_used,
        "source": source,
        "metrics_source": metrics_source,
        "network_ok": network_ok,
        "evidence_grounding": evidence,
        # 2026-09-14：框架前缀避免 GRADE 等级与 CINeMA 评级混读
        "grade_reported": ((f"{grade_framework}: {grade}" if (grade and grade_framework) else grade)
                           or (interp.get("grade") if isinstance(interp.get("grade"), str) else "")),
        # ── P2c ──
        "field_source": field_source,
        "reporting_standards": standards,
        "prisma_source": prisma_source,
        "highly_cited": highly_cited,
        "s2_status": s2_status,
        # ── ref_sections 参考标注 ──
        "ref_sections_used": bool(ref_sections),
    }


if __name__ == "__main__":
    import sys
    _sample = {
        "k": 8, "sm": "OR",
        "pooled": {"estimate_exp": 2.15, "estimate": 0.766, "ci_lower": 1.38, "ci_upper": 3.35},
        "heterogeneity": {"I2": 45.0}, "bias": {"egger_p": 0.12},
    }
    _out = advise_publication(_sample, task="pairwise_meta", topic="EGFR-TKI 一线治疗 NSCLC",
                              interpretation={"conclusion": "合并 OR 显著。", "reviewer_questions": ["是否做 OS/PFS 区分？"]})
    print(json.dumps(_out, ensure_ascii=False, indent=2))
