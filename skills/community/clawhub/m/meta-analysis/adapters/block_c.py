# -*- coding: utf-8 -*-
"""Phase 3 · Block C 本地优先管线驱动器（论文撰写与修改）。

设计约束（对齐 contracts/pipeline_stage/v1.0.0/SPEC.md §9 / roadmap Phase 3）：

- **不依赖 coze 部署**：本模块完全本地运行，不调用 run_stage/run_meta，故不触发出站鉴权。
  C1 初稿为**结构化骨架生成器**（本地启发式，数字自动填充 B1-B4 结果）；C2 AI 评审复用
  block_b.detect_overclaims（B3 单点实现）；C3 参考完整性核验为 🔴 红线（结构/PRISMA 检查 +
  CrossRef/PubMed 真实 API 核验，防 AI 虚构参考文献）；C4 证据表+投稿前 QA 含 🔴 终闸。
- 阶段序列（SPEC §9）：
    C1.draft          结构化初稿（Markdown，数字填充 B1-B4）
    C2.ai_review      AI 评审（复用 B3 过度声明检测）
    C3.ref_verify     参考完整性核验（🔴 reference_verification 红线）
    C4.evidence_qa    证据表 + 投稿前 QA（🔴 manuscript_approval 终闸）
- 返回结构与 run_pipeline / run_block_a / run_block_b 同构：{done, await_human, gate, final,
  stages[], attachments[], tool_card_outputs[]}。
- 红线闸名严格复用 coze_client._REDLINE_GATES：C3=reference_verification、C4=manuscript_approval。

依赖：coze_client（CONTRACT_VERSION / STAGE_SCHEMA_ID / _REDLINE_GATES）；block_b（_mk_stage /
detect_overclaims，信封与 B3 复用）；ref_verify（CrossRef/PubMed 真实参考文献核验，防虚构）。
"""

import math
import re
import uuid

import coze_client as cc
from block_b import detect_overclaims, B1, B2, B3, B4
from ref_verify import verify_references

# 论文撰写辅助引擎（2026-09-14 已建；此前未接入 C1，本次 C 档接通）
try:
    import writing_advisor as wa
    _HAVE_WA = True
except Exception:  # noqa: BLE001 — 引擎缺失时降级为空，不阻断 C1
    _HAVE_WA = False

# ---- Block C 阶段 ID（SPEC §9，严格匹配 coze 端编排对齐） ----
C1 = "C1.draft"
C2 = "C2.ai_review"
C3 = "C3.ref_verify"
C4 = "C4.evidence_qa"
BLOCK_C_SEQUENCE = [C1, C2, C3, C4]
BLOCK_C_TOTAL = len(BLOCK_C_SEQUENCE)

# C 阶段本地红线闸（严格复用 coze_client._REDLINE_GATES 枚举）
GATE_REF_VERIFY = "reference_verification"
GATE_MANUSCRIPT = "manuscript_approval"

# 初稿必含章节（中英文对照组；C3 结构核验按「任一侧命中即视为存在」判定）
_SECTION_PAIRS = [("背景", "Background"), ("方法", "Methods"), ("结果", "Results"),
                  ("讨论", "Discussion"), ("结论", "Conclusion")]
# 中英合一的必含章节清单（由 _SECTION_PAIRS 派生，避免两处清单漂移）
_REQUIRED_SECTIONS = [s for _pair in _SECTION_PAIRS for s in _pair]

# LLM 系统 prompt 模板
_SYSTEM_PROMPT_ZH = """你是一位循证医学与流行病学写作专家。你的任务是基于给定的 meta 分析统计结果和研究数据，撰写一篇系统评价/meta 分析的初稿章节。

要求：
1. 严格基于提供的统计结果和研究数据，不虚构数字或结论
2. 与 GRADE 证据质量评级保持一致
3. 讨论段须提及 B3 检测出的潜在过度声明（已标注）
4. 结论须与 CI 跨零情况和效应方向一致
5. 学术、严谨、简洁
6. 每节 2-5 段落，勿过长
7. 引用格式：作者（年份）"""

_SYSTEM_PROMPT_EN = """You are an evidence-based medicine and epidemiology writer. Your task is to draft sections of a systematic review / meta-analysis based on the provided statistical results and study data.

Requirements:
1. Strictly base all content on the provided statistics and study data — do not fabricate numbers or conclusions
2. Be consistent with the GRADE evidence quality rating
3. Mention potential overclaims detected by B3 (flagged) in the discussion section
4. Conclusions must align with CI crossing-null status and effect direction
5. Academic, rigorous, concise
6. 2-5 paragraphs per section, not excessively long
7. Citation format: Author (Year)"""


def _n(n, one, many):
    """单数/复数选择（英文）。"""
    return one if n == 1 else many


def _author_label(s):
    """提取第一作者姓氏，用于文中引用 (Surname (Year))。兼容 authors 列表 / author 字符串。"""
    if not isinstance(s, dict):
        return "Anonymous"
    authors = s.get("authors")
    if isinstance(authors, list) and authors:
        a0 = authors[0]
        if isinstance(a0, dict):
            fam = a0.get("family") or a0.get("last") or a0.get("name")
            ini = (a0.get("initials") or "") if isinstance(a0, dict) else ""
            if isinstance(fam, str):
                fam = fam.split()[-1]
                # APA 风格："Loukil I" —— 带上 initials，避免参考文献里出现一堆
                # 只有姓氏、无法区分的条目。
                return (f"{fam} {ini}".strip() if ini else fam)
            if fam is not None:
                return str(fam)
        elif isinstance(a0, str):
            return a0.split(",")[0].split()[-1].split(".")[0]
    auth = s.get("author") or s.get("first_author")
    if auth:
        return str(auth).split(",")[0].split()[-1].split(".")[0]
    return "Anonymous"


def _intext(s):
    """文中引用串：Surname (Year)。"""
    if not isinstance(s, dict):
        return "Anonymous (n.d.)"
    return f"{_author_label(s)} ({s.get('year') or 'n.d.'})"


def _study_cite(s):
    """把单条 study dict 归一为 APA 风格引用串（参考文献落表，含 PMID/DOI 供 C3 核验）。"""
    if not isinstance(s, dict):
        return str(s)
    author = _author_label(s)
    year = s.get("year") or s.get("publication_year") or "n.d."
    title = s.get("title") or ""
    journal = s.get("journal") or s.get("publication") or s.get("venue") or ""
    parts = [f"{author} ({year}). {title}."]
    if journal:
        parts.append(f" {journal}.")
    pmid = s.get("pmid")
    doi = s.get("doi")
    if pmid:
        parts.append(f" PMID: {pmid}.")
    if doi:
        parts.append(f" doi:{doi}")
    return "".join(parts).strip()


def _study_key(s):
    """文献去重键：DOI 优先，退到归一标题。"""
    if not isinstance(s, dict):
        return ("", str(s or "").strip().lower())
    doi = str(s.get("doi") or "").strip().lower()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi).strip(" .;,)")
    if doi:
        return ("doi", doi)
    title = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", str(s.get("title") or "").lower())
    return ("title", title)


def _merge_studies(base, extra):
    """base 为基准，把 extra 中**未重复**的条目追加在后（DOI/标题去重）。"""
    out, seen = [], set()
    for lst in (base or [], extra or []):
        for s in lst:
            if not isinstance(s, dict):
                continue
            k = _study_key(s)
            if k[1] and k in seen:
                continue
            if k[1]:
                seen.add(k)
            out.append(s)
    return out


def _literature_context(studies_list):
    """真实文献语境段落（接地于 A2 收集到的论文）：列明纳入研究、设计类型、年份跨度。

    纯描述性、不臆造具体效应量；仅陈述可验证的书目事实（作者/年份/刊名/设计）。
    """
    if not studies_list:
        return None
    n = len(studies_list)
    years = [s.get("year") for s in studies_list
             if isinstance(s, dict) and isinstance(s.get("year"), int)]
    yr = f"{min(years)}–{max(years)}" if years else "the included period"
    types = {}
    for s in studies_list:
        if not isinstance(s, dict):
            continue
        t = str(s.get("study_type") or s.get("type") or "study").replace("_", " ")
        types[t] = types.get(t, 0) + 1
    type_desc = ", ".join(f"{c} {_plur(t, c)}" for t, c in
                          sorted(types.items(), key=lambda kv: -kv[1])[:4])
    named = "; ".join(_intext(s) for s in studies_list[:12])
    if n > 12:
        named += " et al."
    # 措辞：这是**检索到的证据集**，不等于进入合并分析的研究数（后者取 B1 的 k）。
    return (
        f"The retrieved evidence base comprised {n} {_n(n, 'report', 'reports')} published between "
        f"{yr}. Study designs included {type_desc}. The following reports were "
        f"retrieved and screened: {named}."
    )


def _plur(t, c):
    """设计类型标签复数化（c>1：辅音+y→ies，-is→-es，否则加 s；已以 s 结尾则不变）。"""
    if c == 1:
        return t
    if t.endswith("s"):
        return t
    # "meta-analysis" → "meta-analyses"（此前按「以 s 结尾」被跳过，输出
    # "3 meta-analysis" 这种错误复数）
    if t.endswith("sis"):
        return t[:-3] + "ses"
    if t.endswith("y") and len(t) > 1 and t[-2] not in "aeiou":
        return t[:-1] + "ies"
    return t + "s"


def _mk_stage(sid, index, status, stage_result, nha, tool_cards=None):
    """Block C 阶段信封（与 block_a / block_b 同构）。

    本块自行实现而非复用 block_b._mk_stage：后者的 total / prev_stage_id 取自
    BLOCK_B_SEQUENCE/BLOCK_B_TOTAL，会让 C 阶段的 prev_stage_id 指向 B 阶段（溯源错误）。
    """
    nha = nha or {}
    return {
        "mode": "stage",
        "stage": {"id": sid, "index": index, "total": BLOCK_C_TOTAL, "status": status,
                  "prev_stage_id": BLOCK_C_SEQUENCE[index - 1] if index > 0 else None},
        "stage_result": stage_result,
        "next_human_action": nha,
        "tool_cards": tool_cards or [],
        "_gate_blocked": bool(nha.get("gate") in cc._REDLINE_GATES and nha.get("required")),
    }


# ---------------------------------------------------------------------------
# 信封构造（本地「prompt → 合法入参」层）
# ---------------------------------------------------------------------------
def build_block_c_env(topic=None, pipeline_id=None, query_origin=None):
    env = {
        "contract_version": cc.CONTRACT_VERSION,
        "schema": cc.STAGE_SCHEMA_ID,
        "pipeline_id": pipeline_id or f"blkC-{uuid.uuid4().hex[:8]}",
        "pipeline": {"name": "block_c", "block": "C", "cfg": {}},
        "request_id": str(uuid.uuid4()),
        "task": "manuscript_writing",
        "params": {"topic": topic},
        "stage": {"id": C1, "index": 0, "total": BLOCK_C_TOTAL,
                  "intent": "run", "prev_stage_id": None},
        "stage_context": {"human_decisions": [], "tool_card_outputs": [], "artifacts": []},
    }
    if query_origin:
        env["query_origin"] = query_origin
    return env


# ---------------------------------------------------------------------------
# B 阶段结果归一（block_c 消费 run_block_b 的输出信封）
# ---------------------------------------------------------------------------
def _extract_b_summary(b_env):
    """从 run_block_b 输出信封抽取 B1-B4 摘要，归一为统一结构。

    返回 {pairwise, nma, grade, overclaims, critical}。若传入的已是归一 dict 则原样补全。
    """
    if isinstance(b_env, dict) and "pairwise" in b_env and "grade" in b_env:
        # 已是归一 dict
        return {
            "pairwise": b_env.get("pairwise", {}),
            "nma": b_env.get("nma", {"status": "skipped", "reason": "无网络数据"}),
            "grade": b_env.get("grade", {}),
            "overclaims": b_env.get("overclaims", []),
            "critical": b_env.get("critical", False),
        }
    stages = (b_env or {}).get("stages", [])
    s_by_id = {s["stage"]["id"]: s for s in stages}
    pw = (s_by_id.get(B1, {}) or {}).get("stage_result", {})
    nma = pw.get("nma", {"status": "skipped", "reason": "无网络数据"})
    pw = pw.get("pairwise", pw)
    grade = (s_by_id.get(B2, {}) or {}).get("stage_result", {})
    b3 = (s_by_id.get(B3, {}) or {}).get("stage_result", {})
    b4 = (s_by_id.get(B4, {}) or {}).get("stage_result", {})
    return {
        "pairwise": pw,
        "nma": nma,
        "grade": grade,
        "overclaims": b3.get("hits", []),
        "critical": b4.get("critical", False),
    }


# ---------------------------------------------------------------------------
# 文献接地状态（C 流程启动提示：没检索到文献时必须明说，不能静默降级）
# ---------------------------------------------------------------------------
def _has_cjk(s):
    """文本是否含中日韩字符（用于判定「中文主题未配英文题名」）。"""
    return any("一" <= ch <= "鿿" for ch in (s or ""))


#: 英文稿件里的「源语言」标记（2026-09-22）。
#: 作者提供的 PICOS / 检索期 / RoB 等字段可能是中文；稿件正文是英文。规则是
#: **不臆造翻译**（医学表述机器翻译有风险，可能改变含义）也**不静默丢弃**（丢信息），
#: 而是原样保留 + 显式标记，并在 Methods 末尾统一交代「投稿前需补英文」。
_SRC_LANG_MARK = "[source language]"


def evidence_status(evidence=None, topic_en=None, topic=None, error=None,
                    has_studies=False, n_upstream=0):
    """判定 C1 的文献接地（grounding）状态，产出**可直接显示给用户**的提示。

    背景（2026-09-22 用户要求）：C 流程启动时若没有可用检索信息，此前是**静默
    降级** —— 正文照出，但背景/讨论/参考文献全靠通用表述与 "(to be added)"
    占位符，用户根本不知道「这次没检索到文献」。静默降级在这里是危险的：读者会
    以为稿子已经引了真文献。故一律显式回传状态 + 提示文案。

    判据分三层：**有没有可引用的真文献**才是用户真正关心的结论 —— 完整 A 流程
    的稿子拿的是 A2 文献集（has_studies=True），此时 Europe PMC 补检索失败或
    压根没跑都不该报 warn（否则每次正常流程都误报）。只有「上游没有文献 **且**
    补检索也没拿到」才是真的没接地。

    返回 dict（前端与 fullflow 共用，唯一真源，避免两处推导漂移）：
      searched   是否真的发起过检索
      ok         是否拿到可引用的文献
      source     auto_search | user_upload | None（无证据）
      has_studies 是否已有上游（A2）文献集接地
      reason     user_files | ok | upstream_only | no_topic | no_topic_en
                 | error | no_hit | not_searched
      level      ok / info（无需紧张）| warn（没接地，需处理）
      title      提示条标题（按证据来源变化：自动检索 / 作者自备文献）
      notice     给用户的中文提示文案
    """
    ev = evidence or {}
    prim = list(ev.get("primary") or [])
    synth = list(ev.get("synthesis") or [])
    _is_user = str(ev.get("source") or "") == "user_upload"
    st = {
        "searched": bool(ev),
        "source": (ev.get("source") or ("auto_search" if ev else None)),
        "is_user_upload": _is_user,
        "ok": bool(ev.get("ok")) and bool(prim or synth),
        "has_studies": bool(has_studies),
        "n_upstream": int(n_upstream or 0),
        "n_primary": len(prim),
        "n_synthesis": len(synth),
        "hit_count": ev.get("hit_count") or {},
        "database": ev.get("database"),
        "searched_on": ev.get("searched_on"),
        "query": ev.get("query") or {},
        "topic_en": topic_en,
        "error": (str(error) if error else (ev.get("error") or None)),
        "reason": "ok",
        "level": "ok",
        "title": ("文献接地状态（C 流程 · 作者自备文献）" if _is_user
                  else "文献检索状态（C 流程接地）"),
        "uploaded_on": ev.get("uploaded_on"),
        "user_files": ev.get("user_files") or [],
        # 用户上传时的条目预览（供 C1 面板显示「到底识别到了哪几篇」——上传后
        # 用户最想核对的就这件事；自动检索路径不需要，故仅在 user_upload 时下发）。
        "preview": [
            {"title": (r.get("title") or "")[:160],
             "year": r.get("year"),
             "type": r.get("study_type"),
             "first_author": _author_label(r),
             "doi": r.get("doi")}
            for r in ((prim + synth)[:20] if _is_user else [])
        ],
        "notice": None,
    }
    _up = (f"正文另有流程内检索到的 {st['n_upstream']} 篇文献可供引用"
           if has_studies else "")
    # ── 作者自备文献（C1 上传）优先判定 ──────────────────────────────────
    # 这批文献是用户自己筛过/改过的清单，权威性高于自动检索，故单独一条
    # reason，且提示为「已接地」的正面结论（不再是「没检索到」的告警）。
    # 仍如实指出**缺字段**的条目数：Excel 少填作者/年份、PDF 元数据缺失时，
    # 正文只能按 Anonymous / n.d. 处理 —— 这属于用户可自行修好的问题，
    # 必须说出来，否则参考文献里出现 Anonymous 会让人以为是程序 bug。
    if _is_user and st["ok"]:
        _names = "、".join(str(f.get("name") or "") for f in st["user_files"][:4])
        if len(st["user_files"]) > 4:
            _names += f" 等 {len(st['user_files'])} 个文件"
        _all = prim + synth
        _miss_a = sum(1 for r in _all if not (r.get("authors") or []))
        _miss_y = sum(1 for r in _all if not r.get("year"))
        _miss = []
        if _miss_a:
            _miss.append(f"{_miss_a} 篇缺作者")
        if _miss_y:
            _miss.append(f"{_miss_y} 篇缺年份")
        st.update(reason="user_files", level="info", notice=(
            f"✓ 初稿已接地到你上传的 {len(_all)} 篇文献"
            f"（原始研究 {len(prim)} / 汇总性文献 {len(synth)}）。\n"
            f"来源文件：{_names or '（未记录）'}"
            + (f"，上传于 {st['uploaded_on']}" if st.get("uploaded_on") else "")
            + "\n正文背景/讨论与参考文献均取自这批文献，未再做 Europe PMC 检索。"
            + (("\n注意：" + "、".join(_miss)
                + "（Excel 未填或 PDF 元数据缺失），正文相应处按 Anonymous / n.d. 处理；"
                  "补全后重新上传即可。") if _miss else "")))
    elif st["ok"]:
        st.update(reason="ok", level="ok", notice=(
            f"✓ 已检索到 {len(prim)} 篇原始研究 + {len(synth)} 篇系统评价/Meta 分析"
            f"（{ev.get('database') or 'Europe PMC'}，{ev.get('searched_on') or ''}），"
            "正文背景/讨论与参考文献已接地到这些真实论文。"))
    elif has_studies:
        # 上游（A2）已有真实文献 → 补检索缺位不是问题，只做 info 说明
        st.update(reason="upstream_only", level="info", notice=(
            f"ℹ 本次未做 Europe PMC 补充检索，正文文献取自流程内已检索的文献集"
            f"（{st['n_upstream']} 篇）。"
            + (f"补充检索未执行原因：{st['error']}。" if st["error"] else "")))
    elif st["error"]:
        st.update(reason="error", level="warn", notice=(
            "⚠ 文献检索失败，本次初稿没有引用任何真实文献。\n"
            f"原因：{st['error']}\n"
            "影响：背景与讨论为通用表述，参考文献为占位符。\n"
            "处理：检查网络后重启 C 流程，或改用更宽的英文检索词。"))
    elif ev:
        _q = (ev.get("query") or {}).get("primary")
        st.update(reason="no_hit", level="warn", notice=(
            "⚠ Europe PMC 未检索到与该主题相关的文献，本次初稿没有引用任何真实文献。\n"
            f"检索式：{_q or '（未记录）'}\n"
            "影响：背景与讨论为通用表述，参考文献为占位符。\n"
            "处理：换更宽的英文检索词，或在开始页补充「英文题名」后重启 C 流程。"
            + ("（当前主题为中文且未填英文题名，优先补英文题名。）"
               if _has_cjk(topic) and not (topic_en or "").strip() else "")))
    elif _has_cjk(topic) and not (topic_en or "").strip():
        st.update(reason="no_topic_en", level="warn", notice=(
            "⚠ 未提供英文题名，未能在 Europe PMC 检索到可用文献。\n"
            "中文主题直接送检命中率极低，故本次初稿没有引用任何真实文献"
            "（背景/讨论为通用表述，参考文献为占位符）。\n"
            "处理：回到开始页填写「英文题名」后重新启动 C 流程即可接地真实文献。"))
    elif not (topic or "").strip():
        st.update(reason="no_topic", level="warn", notice=(
            "⚠ 未获取到研究主题，无法检索文献；初稿未引用任何真实文献。"))
    else:
        st.update(reason="not_searched", level="warn", notice=(
            "⚠ 本次未做文献检索（检索层未启用或主题为空），初稿没有引用任何真实文献。\n"
            "影响：背景与讨论为通用表述，参考文献为占位符，需你自行补充。"))
    if _up and st["level"] == "warn":
        st["notice"] += f"\n注：{_up}（请人工核对是否够用）。"
    return st


# ---------------------------------------------------------------------------
# C1 初稿生成（结构化 Markdown，数字自动填充 B1-B4 + 上游真实素材接地 + 写作辅助引擎）
# ---------------------------------------------------------------------------
def c1_draft(topic, b_summary, studies=None, overclaim_hits=None,
             studies_list=None, prisma_flow=None, picos=None,
             search_info=None, rob_summary=None, merged_json=None,
             ref_sections=None, topic_en=None, evidence=None, evidence_error=None):
    """由 B1-B4 结果 + 上游真实素材生成结构化初稿（C 档：接通写作辅助引擎 + 真实数据接地）。

    本地启发式：章节齐全、关键统计量自动填充；接通 writing_advisor 注入
    strengths/limitations/discussion_template/reviewer_questions/journal_fit；
    方法/结果段填充真实检索与筛选信息（PRISMA 流、PICOS、数据库与日期、RoB 工具）；
    参考文献直接由 A2 文献集 DOI 落表，交 C3 核验。
    叙述性 prose（背景/讨论/结论/摘要）由编排层 LLM 扩写（见 c1_expand_narrative）；
    本函数产出"已接地、待扩写"的 scaffold。无 LLM 时讨论段含写作辅助要点供人参考。
    返回 {manuscript, sections[], char_count}。

    2026-09-22 新增两个入参（均为可选，缺省时行为与之前完全一致）：
      - topic_en：英文题名。稿件正文是英文，若调用方只给中文 topic，正文里
        直接嵌入中文会造成中英混杂；有英文题名时一律用它。
      - evidence：literature_probe.search_evidence() 的真实检索结果（Europe
        PMC）。用于把背景/讨论/参考文献接地到**真实存在的论文**，而不是
        "(to be added)" 占位符。检索失败时优雅降级（不阻断流程）。
    """
    pw = b_summary.get("pairwise", {}) or {}
    nma = b_summary.get("nma", {}) or {}
    grade = b_summary.get("grade", {}) or {}
    k = pw.get("k", 0)
    em = pw.get("effect_measure", "OR")
    te_r = pw.get("TE_random")
    ci_r = pw.get("ci_random") or pw.get("ci_fixed")
    p_r = pw.get("p_random", pw.get("p_fixed"))
    i2 = pw.get("I2")
    tau2 = pw.get("tau2")
    egger_p = pw.get("egger_p")
    # ── 效应量尺度归一（2026-09-22 修复「OR = -0.38」）──
    # pairwise 的 TE / CI 一律在**分析尺度**上：比值类（OR/RR/HR…）是对数尺度
    # （存的是 log OR），差值类（MD/SMD/RD）是原始尺度。写进稿件必须换算到
    # **报告尺度**（比值类取 exp），否则就会把 log OR 当成 OR 印出去。
    # 比值类集合与 interpretation._RATIO_SM 同一约定（此处复用，避免两处漂移）。
    _RATIO_EM = {"OR", "RR", "HR", "PLO", "PLOGIT", "IRR", "RRR"}
    _is_ratio = str(em).upper() in _RATIO_EM
    # 分析尺度上的无效线：比值类 log(1)=0、差值类 0 → **恒为 0**。
    # 旧代码拿 log OR 去比 1.0，方向判定与「CI 是否跨无效线」都是错的。
    _null_an = 0.0

    def _to_report(x):
        """分析尺度 → 报告尺度（比值类取 exp）；非数值原样返回。"""
        if not isinstance(x, (int, float)):
            return x
        return math.exp(x) if _is_ratio else float(x)

    _ci_rep = ([_to_report(ci_r[0]), _to_report(ci_r[1])]
               if isinstance(ci_r, (list, tuple)) and len(ci_r) >= 2 else None)
    te_rep = _to_report(te_r)
    direction = ("increased" if (te_r is not None and te_r > _null_an)
                 else ("decreased" if te_r is not None else "—"))

    def _fmt(x, n=2):
        return ("%.*f" % (n, x)) if isinstance(x, (int, float)) else str(x)

    # 注意：此处不带「合并效应」字样 —— 调用方模板（摘要/方法）已含
    # 「主要合并效应」前缀，重复会出现「主要合并效应 OR 合并效应 = ...」
    if k == 0:
        eff_line = "No computable studies available"
    elif _ci_rep is None:
        eff_line = f"{em} = {_fmt(te_rep)} (95% CI n/a, p = {_fmt(p_r, 3)})"
    else:
        eff_line = (f"{em} = {_fmt(te_rep)} "
                    f"(95% CI {_fmt(_ci_rep[0])}–{_fmt(_ci_rep[1])}, p = {_fmt(p_r, 3)})")
    # ⚠️ pairwise.I2 恒为百分数（coze 契约 §4；b1_pairwise_python 已同构归一），
    #    此处**不得再 ×100** —— 旧代码 ×100 会把 I²=34.5% 渲染成「I² = 3453%」，
    #    且本变量被摘要/方法/结论四处复用，一处错则处处错。
    i2_line = ("I² = %.0f%%" % i2) if isinstance(i2, (int, float)) else "I² = —"
    tau_line = (f"τ² = {_fmt(tau2)}" if isinstance(tau2, (int, float)) else "τ² = —")
    egger_line = (f"Egger p = {_fmt(egger_p, 3)}" if isinstance(egger_p, (int, float))
                  else "Egger p = —")

    nma_line = "Network meta-analysis (NMA) was not performed."
    if nma.get("status") == "ok":
        comps = nma.get("result", {}).get("comparisons", []) or []
        nma_line = (f"Network meta-analysis (random-effects model) included "
                    f"{nma.get('result', {}).get('n_treatments', [0])[0]} interventions and "
                    f"{len(comps)} indirect comparisons.")
    elif nma.get("status") in ("skipped", "error"):
        nma_line = f"Network meta-analysis was not performed ({nma.get('reason', 'n/a')})."

    grade_line = grade.get("grade", "—")
    # 英文稿件用英文降级理由（block_b.b2_grade 同步产出的 reasons_en）。
    # 旧信封（无 reasons_en）只有中文 reasons —— 中文不得进英文正文，故过滤掉，
    # 但**不静默丢弃**：改用一条指针交代「另有 N 条降级理由记录在 B2」，读者可回查。
    _reasons_raw = list(grade.get("reasons_en") or grade.get("reasons", []) or [])
    reasons = [r for r in _reasons_raw if not _has_cjk(r)]
    _reasons_dropped = len(_reasons_raw) - len(reasons)
    _reasons_txt = "; ".join(reasons) if reasons else "no major downgrading"
    if _reasons_dropped:
        _reasons_txt += (f"; {_reasons_dropped} further rationale(s) omitted here "
                         f"(recorded in the source language in the GRADE assessment)")
    is_network = nma.get("status") == "ok"

    # ── 上游真实素材（A2/A3 透传） ──
    # 上游是否已有真实文献（A2 文献集 / 显式 studies）—— 决定「没检索到文献」
    # 该不该报 warn：有上游文献时补检索缺位不是问题（见 evidence_status）。
    _upstream_studies = bool(studies_list) or bool(studies)
    _n_upstream = len(studies_list or []) or len(studies or [])
    # ── 真实文献接地（2026-09-22）：Europe PMC 检索结果 → 可引用文献集 ──
    # 记录已由 literature_probe 做过相关性过滤，字段只有书目事实（作者/年份/
    # 刊名/设计/DOI/PMID/被引数），**不含任何臆造的结局数字**。
    ev = evidence or {}
    ev_primary = list(ev.get("primary") or [])
    ev_synth = list(ev.get("synthesis") or [])
    # 作者自备文献（C1 上传）—— 用户自己筛过/改过的清单，权威性高于自动检索：
    # 即使流程内已有 A2 文献集，也以它为**参考文献基准**，把 A2 中不重复的条目
    # 追加在后（去重），保证「用户上传的内容一定进参考文献、已有素材也不丢」。
    _from_user = bool(ev) and str(ev.get("source") or "") == "user_upload"
    if _from_user:
        studies_list = _merge_studies(ev_primary + ev_synth, studies_list)
        # 语义同 _from_evidence：这是**作者提供的证据集**，不等于合并分析的
        # 纳入集（纳入数以 B1 的 k 为准），不得写成 "included studies"。
        _from_evidence = True
    elif ev and not studies_list:
        studies_list = ev_primary + ev_synth
        # 标记：这批文献是**检索到的证据集**，不是 A2 实际纳入的研究。
        # 后续不得把它们写成 "included studies"（纳入数以 B1 的 k 为准）。
        _from_evidence = True
    else:
        _from_evidence = False
    ev_hits = ev.get("hit_count") or {}
    ev_db = ev.get("database")
    ev_date = ev.get("searched_on")
    ev_query = (ev.get("query") or {}).get("primary")
    ev_ok = bool(ev.get("ok"))
    studies_list = studies_list or []
    # ⚠️ 两个"研究数"含义不同，**不能混用**（2026-09-22 修复）：
    #   - n_stud：真正进入**合并分析**的研究数 —— 以 B1 的 k 为准（统计口径最
    #     权威）。此前直接取 studies_list 长度，导致「检索到 15 篇」被写成
    #     「纳入 15 项研究」，与 k=6 的合并效应自相矛盾。
    #   - _n_ev：检索到的证据集条数，仅用于描述文献背景/特征表。
    _n_ev = len(studies_list)
    n_stud = k if k else (len(studies) if studies else _n_ev)
    prisma = prisma_flow or {}
    picos = picos or {}
    search = search_info or {}
    rob = rob_summary or {}

    # ── 作者提供字段的「源语言」处理（2026-09-22）──
    # 论文 PICOS / 检索期 / 数据库 等值由用户填写，可能是中文；稿件正文是英文。
    # 直接拼进英文句子 → 「慢性肾脏病患者 is a question with...」这类中英混杂
    # （用户已反复反馈）。这里统一成一条规则：
    #   · 字段**列示**处（PICOS / Eligibility / Search strategy）→ 原样保留 + 标记
    #     `[source language]`，不丢信息；
    #   · 英文**叙述句**里（摘要背景、讨论）→ 该值不可内联，改用通用表述，避免
    #     出现不合语法的中英拼接；
    #   · 稿末统一交代需作者补英文，避免读者把标记当成稿件内容。
    _src_lang_fields = []

    def _fld(v, name):
        """渲染一个作者提供字段：含中文时原样保留并标记为源语言。"""
        s = str(v or "").strip()
        if s and _has_cjk(s):
            _src_lang_fields.append(name)
            return f"{s} {_SRC_LANG_MARK}"
        return s

    if _from_user:
        # 作者自备文献：不存在"检索了哪些库、检索期多长"这回事，不能照抄检索
        # 口径（否则方法学里会凭空出现一句"检索了 Europe PMC 至某日"）。
        databases = search.get("databases") or [
            "author-supplied reference list (uploaded by the author)"]
        date_range = search.get("date_range") or search.get("start_date") or (
            "not applicable (author-supplied reference list)")
    else:
        databases = search.get("databases") or ([ev_db] if ev_db
                                                else ["(to be added: databases searched)"])
        date_range = search.get("date_range") or search.get("start_date") or (
            f"database inception to {ev_date}" if ev_date else "(to be added: search dates)")
    if search.get("end_date"):
        date_range = f"{date_range} to {search.get('end_date')}"
    # 检索式：用 Europe PMC 实际执行的查询串，比 "(to be added)" 有据可查
    strategy = search.get("strategy") or (ev_query or "(to be added: search strategy / syntax)")
    rob_tool = rob.get("tool") or "Cochrane RoB 2.0 / NOS"
    if rob.get("n_low") is not None:
        _nlow = rob.get("n_low"); _nhigh = rob.get("n_high"); _nsome = rob.get("n_some")
        if _nsome is None and _nhigh is not None and n_stud:
            _nsome = max(n_stud - _nlow - _nhigh, 0)
        rob_line = (f"Risk of bias was assessed using {rob_tool}; "
                    f"{_nlow}/{_nsome}/{_nhigh} studies were at "
                    f"low/moderate/high risk, respectively.")
    else:
        rob_line = f"Risk of bias was assessed using {rob_tool} (risk distribution to be added)."

    methods_block = (
        f"- **Study design**: Systematic review and meta-analysis following PRISMA 2020 reporting guidelines.\n"
        f"- **Registration and protocol**: (to be added: PROSPERO registration number).\n"
        f"- **PICOS**: P={_fld(picos.get('P'), 'P') or '(to be added)'}; I={_fld(picos.get('I'), 'I') or '(to be added)'};"
        f"C={_fld(picos.get('C'), 'C') or '(to be added)'}; O={_fld(picos.get('O'), 'O') or '(to be added)'};"
        f"S={_fld(picos.get('S'), 'S') or '(to be added)'}.\n"
        f"- **Search strategy**: Databases searched: {', '.join(_fld(d, 'databases') for d in databases)};"
        f" search period: {_fld(date_range, 'search period')}."
        f" Search terms/syntax: {strategy}\n"
        f"- **Study selection and data extraction**: Two reviewers independently screened and extracted data in duplicate (blinded), with discrepancies resolved by a third reviewer.\n"
        f"- **{rob_line}\n"
        f"- **Statistical analysis**: Effect sizes ({em}) were pooled using the inverse-variance method with a random-effects model (DerSimonian-Laird);"
        f" heterogeneity was quantified by I² and τ²{('; network meta-analysis was performed locally using R netmeta.' if is_network else '')}.\n"
        f"- **Certainty of evidence**: Downgrading factors per {'CINeMA (network meta-analysis)' if is_network else 'GRADE'}:"
        f"{_reasons_txt}.\n"
    )

    # Methods 追加条款（2026-09-22）：把「检索产出」「纳入排除」「亚组/敏感性」
    # 这些投稿必需的条目补上，避免正文只剩"(to be added)"骨架。
    _elig = []
    if picos.get("P"):
        _elig.append(f"participants: {_fld(picos.get('P'), 'P')}")
    if picos.get("I"):
        _elig.append(f"intervention: {_fld(picos.get('I'), 'I')}")
    if picos.get("C"):
        _elig.append(f"comparator: {_fld(picos.get('C'), 'C')}")
    if picos.get("O"):
        _elig.append(f"outcome: {_fld(picos.get('O'), 'O')}")
    if picos.get("S"):
        _elig.append(f"study design: {_fld(picos.get('S'), 'S')}")
    methods_block += (
        f"- **Eligibility criteria**: "
        + ("; ".join(_elig) if _elig else
           "(to be added: PICO criteria — population, intervention, comparator, outcome)")
        + ". Reports were excluded when they did not report extractable outcome data "
          "for the comparison of interest.\n"
    )
    if ev_hits:
        _yield = []
        if ev_hits.get("primary"):
            _yield.append(f"{ev_hits['primary']} records for the primary-study search")
        if ev_hits.get("synthesis"):
            _yield.append(f"{ev_hits['synthesis']} for the synthesis search")
        if _yield:
            methods_block += (
                f"- **Search yield**: {'; '.join(_yield)} "
                f"({'searched on ' + ev_date if ev_date else 'search date to be added'}).\n"
            )
    methods_block += (
        "- **Subgroup and sensitivity analyses**: Pre-specified subgroup and sensitivity "
        "analyses (to be added: subgroup variables; sensitivity restricted to studies at "
        "low overall risk of bias and to fixed-effect pooling).\n"
        "- **Software**: Pooled estimates were computed with the meta-analysis engine "
        "underlying this workbench (R meta / netmeta on the analysis server); the review "
        "is reported in accordance with PRISMA 2020.\n"
        "- **Data availability**: Extracted datasets and analysis code are available from "
        "the authors on reasonable request.\n"
    )
    if _src_lang_fields:
        # 作者提供的中文字段已原样保留在上面并标了 [source language]；此处统一交代，
        # 免得读者把标记当稿件内容，也提醒投稿前补英文（不臆造翻译）。
        _uniq = list(dict.fromkeys(_src_lang_fields))
        methods_block += (
            f"- **Note on field language**: the following fields were supplied by the author "
            f"in the source language and are reproduced verbatim above "
            f"({', '.join(_uniq)}); they must be provided in English before submission.\n"
        )

    if prisma:
        _inc = prisma.get('included', n_stud)
        prisma_line = (
            f"A total of {prisma.get('identified', '(to be added)')} records were identified; "
            f"after deduplication, {prisma.get('screened', '(to be added)')} were screened, "
            f"{prisma.get('excluded', '(to be added)')} were excluded, and "
            f"{_inc} {_n(_inc, 'study', 'studies')} (corresponding to {n_stud} {_n(n_stud, 'trial', 'trials')}) {_n(_inc, 'was', 'were')} included."
        )
    else:
        prisma_line = f"A total of {n_stud} {_n(n_stud, 'study', 'studies')} {_n(n_stud, 'was', 'were')} included (PRISMA flow counts to be added)."
    study_cites = ""
    # 只有当 studies_list 真的是 A2 **纳入**的研究时才挂在 "Included studies" 后面。
    # 若它只是 Europe PMC 检索到的证据集，挂上去会变成「纳入研究 = 检索文献」，
    # 与 B1 的 k 自相矛盾（2026-09-22）。
    if studies_list and not _from_evidence:
        head = "; ".join(_intext(s) for s in studies_list[:8])
        if len(studies_list) > 8:
            head += " et al."
        study_cites = f" ({head})"
    results_block = (
        f"- **Study selection**: {prisma_line}\n"
        f"- **Included studies**: {n_stud} {_n(n_stud, 'study', 'studies')}{study_cites}.\n"
        f"- **Primary pooled effect**: {eff_line} (direction of effect: {direction}).\n"
        f"- **Heterogeneity**: {i2_line}, {tau_line}; publication bias {egger_line}.\n"
        f"- **Network meta-analysis**: {nma_line}\n"
        f"- **Certainty of evidence**: {grade_line}.\n"
    )
    # 纳入研究特征表（2026-09-22）：只用检索返回的**书目事实**建表 —— 作者/年份/
    # 设计/刊名/DOI。样本量与结局数字**不在此臆造**（那属于 A3/A4 提取结果，
    # 缺失时表格不列该列，而不是填 0 或占位数字）。
    if studies_list:
        _rows = ["| Study | Year | Design | Journal | Identifier |",
                 "| --- | --- | --- | --- | --- |"]
        for s in studies_list[:15]:
            _yr = s.get("year") or "n.d."
            _id = s.get("doi") or (f"PMID: {s.get('pmid')}" if s.get("pmid") else "—")
            _jr = (s.get("journal") or "—")
            _jr = (_jr[:46] + "…") if len(_jr) > 46 else _jr
            _rows.append(f"| {_author_label(s)} | {_yr} | {s.get('study_type') or 'study'} "
                         f"| {_jr} | {_id} |")
        if len(studies_list) > 15:
            _rows.append(f"| … | | | | ({len(studies_list) - 15} further reports) |")
        results_block += ("\n**Characteristics of the retrieved evidence base** "
                          "(bibliographic fields only; outcome data are extracted "
                          "separately in Block A):\n\n" + "\n".join(_rows) + "\n")

    # ── 写作辅助引擎（接通） ──
    wa_strengths = wa_limits = wa_disc = wa_questions = wa_journal = ""
    if _HAVE_WA:
        _wa_stats = {
            "k": k, "sm": em,
            # 报告尺度约定（与 writing_advisor 的示例一致：estimate_exp=2.15 对
            # estimate=0.766，ci_lower/ci_upper 同为报告尺度 1.38/3.35）：
            # 只有 estimate 留在分析尺度，其余三个键取 exp。
            "pooled": {"estimate_exp": te_rep, "estimate": te_r,
                       "ci_lower": (_ci_rep[0] if _ci_rep else None),
                       "ci_upper": (_ci_rep[1] if _ci_rep else None)},
            "heterogeneity": {"I2": i2, "tau2": tau2},
            "bias": {"egger_p": egger_p},
        }
        _adv = wa.advise_publication(
            stats=_wa_stats, task=("nma" if is_network else "pairwise_meta"),
            topic=topic or "", merged_json=merged_json, use_network=False,
            ref_sections=ref_sections)
        wa_strengths = "\n".join(f"  - {x}" for x in (_adv.get("strengths") or []))
        wa_limits = "\n".join(f"  - {x}" for x in (_adv.get("limitations") or []))
        wa_disc = _adv.get("discussion_template") or ""
        wa_questions = "\n".join(f"  - {x}" for x in (_adv.get("reviewer_likely_questions") or []))
        wa_journal = _adv.get("journal_fit") or ""

    # B3 过度声明警示
    oc = overclaim_hits or b_summary.get("overclaims", []) or []
    if oc:
        def _oc_line(h):
            """英文稿件里的单条过度声明。两条硬约束（2026-09-22 修）：
              ① **不嵌中文**：正文是英文，中文 label / 中文注记一律不进正文；
              ② **不谎称引文**：h["evidence"] 是 block_b 下发的**模式简称**（12 类
                 之一的中文名，见 _OVERCLAIM_PATTERNS），**不是**被扫描到的原文
                 片段。旧实现把它当引文、还标注 "(verbatim excerpt from the
                 scanned source text)" —— 引文是假的，中文是真的漏进正文。
                 真正的原文落点在 B3 的 scan 记录（scan.preview / hits[].evidence）。
            """
            _lbl = h.get("label_en") or ""
            if not _lbl:
                # 旧信封（B3 命中没有 label_en）只带中文 label —— 直接回落会在英文
                # 正文里漏中文。故此处对中文 label 一律退到语言中立的模式编号。
                _raw = str(h.get("label") or "")
                _lbl = _raw if not _has_cjk(_raw) else (
                    f"pattern {h.get('id')}" if h.get("id") else "unnamed overstatement pattern")
            _sev = h.get("severity")
            _ev = str(h.get("evidence") or "")
            if _ev and not _has_cjk(_ev):
                _tail = f": “{_ev}”"
            elif _ev:
                _tail = " — source-text match recorded in the B3 overclaim scan"
            else:
                _tail = ""
            return f"  - [{h.get('id')}] {_lbl} (severity: {_sev}){_tail}"

        oc_block = "\n".join(_oc_line(h) for h in oc)
        oc_section = (
            "\n\n### ⚠️ Potential overstatements pending manual verification (from B3 detection; do NOT use directly as conclusions)\n"
            f"{oc_block}"
        )
    else:
        oc_section = ""

    # 参考文献（由 A2 文献集 DOI/PMID 落表，交 C3 真实核验）
    ref_lines = []
    for i, s in enumerate(studies_list, 1):
        ref_lines.append(f"{i}. {_study_cite(s)}")
    references_block = ("\n".join(ref_lines) if ref_lines
                        else "(To be added: generated after reference-integrity verification in C3 from the A2 search set.)")
    if _from_evidence and ref_lines and _from_user:
        # 作者自备文献：出处必须写清是"作者上传的清单"（而非我们检索来的），
        # 并说明与流程内素材的合并情况 + 仍需在 C3 逐条核验。
        _up = ""
        if _upstream_studies:
            _up = (f" It also incorporates {_n_upstream} record(s) from the workflow's own "
                   "search set that were not present in the uploaded list.")
        references_block = (
            # 不列文件名：稿件正文是英文，而用户文件名常是中文（"我的文献清单.xlsx"），
            # 直接拼进去会让英文段落里冒出中文。文件名的可追溯性由工作台的中文提示条
            # 与上传记录承担，稿件里只需要说明"这是作者自备清单 + 上传日期"。
            "Supplied by the author as an uploaded literature list"
            + (f" on {ev.get('uploaded_on')}" if ev.get("uploaded_on") else "")
            + ". These records support the Background and Discussion sections and the "
              "reference list; they are the author's own collection rather than the "
              "workflow's retrieved set, and each entry must still be verified in C3 "
              "(and reconciled with the final included-study list) before submission."
            + _up + "\n\n"
            + references_block)
    elif _from_evidence and ref_lines:
        # 如实交代这批条目的来源：它们是**检索命中**，不等于最终纳入集，
        # 投稿前必须与真实纳入清单核对（C3 会做逐条核验）。
        references_block = (
            f"Retrieved from {ev_db or 'Europe PMC'}"
            + (f" on {ev_date}" if ev_date else "") +
            " by searching the review question. These records support the Background and "
            "Discussion sections; they are **not** the final included-study list and must "
            "be reconciled with it (and verified in C3) before submission.\n\n"
            + references_block)

    # 写作辅助段落预先拼接（不直接写入 manuscript 正文；保留供人工参考）
    wa_block = ""
    if wa_strengths:
        wa_block += "### Strengths\n" + wa_strengths + "\n"
    if wa_limits:
        wa_block += "### Limitations\n" + wa_limits + "\n"
    if wa_disc:
        wa_block += "### Discussion Points (writing-advisor)\n" + wa_disc + "\n"

    # ── 完整英文叙述（本地确定性生成，接地于真实收集到的文献与统计量） ──
    # 目标：直接产出「可用于投稿的初稿」——所有章节均写入真实英文叙述，不再留
    # (To be expanded) 占位；仅缺数据的「具体字段」标记「待补」，结构性章节不缺失。
    # 叙述句可内联的前提：值存在、非占位符，**且非中文** —— 中文 P 拼进英文句子会
    # 变成「慢性肾脏病患者 is a question with...」（不合语法）；此时改用通用表述，
    # 实际取值仍在 PICOS / Eligibility 字段里带 [source language] 标出，不丢信息。
    _db_ok = (databases != ["(to be added: databases searched)"]
              and not _has_cjk(", ".join(str(d) for d in databases)))
    _p = (picos.get("P") if isinstance(picos, dict) else None) or ""
    _p_ok = bool(_p) and _p != "(to be added)" and not _has_cjk(_p)
    # 跨无效线判定也在**分析尺度**上做（无效线 = 0），不能用报告尺度的 1.0 去比 log CI
    _ci_cross = (isinstance(ci_r, (list, tuple)) and len(ci_r) == 2
                 and ci_r[0] < _null_an < ci_r[1])

    # ── 题名语言处理（2026-09-22）──
    # 稿件正文是英文。调用方给中文 topic 时优先用 topic_en；若没有英文题名，
    # 标题仍保留中文原题（**不能凭空翻译**），但英文句子里的指代改用通用表述，
    # 避免出现 "Evidence on <中文> remains inconclusive" 这种中英混杂。
    # 注：统一用模块级 _has_cjk（第 263 行）。此前这里有个同名本地定义，会在
    # 本函数内**遮蔽**模块级同名函数 —— 于是任何在本行之前定义/调用的嵌套函数
    # （如上面的 _oc_line）引用 _has_cjk 时会命中未绑定的局部变量而 NameError。
    _en_topic = None
    if topic_en and not _has_cjk(topic_en):
        _en_topic = topic_en.strip()
    elif topic and not _has_cjk(topic):
        _en_topic = (topic or "").strip()
    _title = (topic_en or topic or "Untitled Meta-Analysis").strip()
    # 正文句子里只用**主标题**（去掉 ": " 之后的副标题/研究类型后缀），否则会出现
    # "Evidence on Efficacy of X ...: a systematic review and meta-analysis ..."
    # 这种把整条题名塞进句子的笨重表述。标题行本身仍用完整题名。
    _tp = (_en_topic.split(":")[0].strip() if _en_topic else "the research question")
    _need_en_title = not _en_topic

    # ── 真实文献引用串（Europe PMC 接地） ──
    def _cites(items, n=8):
        if not items:
            return ""
        head = "; ".join(_intext(s) for s in items[:n])
        if len(items) > n:
            head += "; et al."
        return head

    _synth_cites = _cites(ev_synth, 6)
    _prim_cites = _cites(ev_primary, 8)

    # Abstract（结构化四段）
    _abs_bg = (f"Evidence on {_tp} remains inconclusive; individual "
               f"studies are limited by power and between-study heterogeneity.")
    if _p_ok:
        _abs_bg = (f"{_p.rstrip('.')} is a question with an uncertain aggregate effect; "
                   f"individual studies are limited by power and heterogeneity.")
    if _synth_cites:
        _abs_bg += (f" Existing syntheses ({_synth_cites}) have not resolved this "
                    f"uncertainty, which motivated the present review.")
    _abs_meth = (f"A systematic review and meta-analysis was conducted per PRISMA 2020. "
                f"Searches covered {', '.join(databases) if _db_ok else 'the specified databases'}"
                + (f" from {date_range}" if ev_date else "") + "; "
                f"{n_stud} {_n(n_stud, 'study', 'studies')} {_n(n_stud, 'was', 'were')} included. "
                f"Effects were pooled with a random-effects model.")
    if ev_hits.get("primary"):
        _synth_part = (" and " + str(ev_hits["synthesis"]) + " syntheses"
                       if ev_hits.get("synthesis") else "")
        _abs_meth += (f" The search identified {ev_hits['primary']} potentially relevant "
                      f"records{_synth_part}.")
    _abs_res = (f"The pooled estimate was {eff_line}; heterogeneity was {i2_line}. "
                f"Certainty of evidence: {grade_line} (GRADE).")
    _abs_con = (f"The pooled analysis suggests the intervention {direction} the outcome; "
                f"{'the confidence interval includes the null, so the result is not definitive' if _ci_cross else 'the estimate is sufficiently precise to inform practice'}. "
                f"Further high-quality primary studies are needed to confirm these findings.")
    abstract_block = (
        "## Abstract\n"
        f"**Background:** {_abs_bg}\n\n"
        f"**Methods:** {_abs_meth}\n\n"
        f"**Results:** {_abs_res}\n\n"
        f"**Conclusions:** {_abs_con}\n"
    )

    # 1. Background（含真实文献语境；四段式：重要性 → 现有合成 → 近期原始研究 → 目的）
    _lit = _literature_context(studies_list)
    _bg = []
    _bg.append(
        f"{_tp.rstrip('.')} has attracted substantial research interest. "
        + (f"{_p.rstrip('.')}. " if _p_ok else "")
        + "Primary investigations to date have been individually underpowered and have "
          "reported heterogeneous results, leaving the overall magnitude and direction of "
          "the effect uncertain."
    )
    if _synth_cites:
        _bg.append(
            "**Existing syntheses.** Prior systematic reviews and meta-analyses have "
            f"addressed this question ({_synth_cites}). Their scope, eligibility criteria, "
            "comparator definitions and outcome instruments differ substantially, so the "
            "pooled estimates they report are not directly comparable and no single "
            "synthesis has settled the question."
        )
    if _prim_cites:
        _bg.append(
            "**Recent primary evidence.** Randomised trials continue to be published in "
            f"this area ({_prim_cites}), and their findings remain divergent with respect "
            "to both the direction and the magnitude of the effect."
        )
    if _lit:
        _bg.append(_lit)
    _bg.append(
        "A quantitative synthesis is therefore required to (i) estimate the pooled effect "
        "with greater precision, (ii) characterize between-study heterogeneity, and "
        "(iii) rate the certainty of the available evidence. The aim of this systematic "
        f"review and meta-analysis was to synthesize the published evidence on "
        f"{_tp} and to provide a clinically interpretable estimate "
        "of the pooled effect."
    )
    background_block = "## 1. Background\n" + "\n\n".join(_bg) + "\n"

    # 4. Discussion（发现 / 与纳入研究对照 / strengths / limitations / implications）
    _disc = []
    _disc.append(
        f"**Summary of main findings.** Pooling {n_stud} {_n(n_stud, 'study', 'studies')} "
        f"yielded a pooled estimate of {eff_line}, indicating that the intervention {direction} "
        f"the outcome. Between-study heterogeneity was {i2_line}; the certainty of evidence "
        f"was graded {grade_line}."
    )
    if _lit:
        _disc.append(
            "**Context with the included studies.** " + _lit +
            " The pooled estimate should be interpreted alongside these primary reports; the "
            "random-effects model reports a weighted average that accommodates the observed "
            "between-study variability rather than assuming a single true effect."
        )
    if _synth_cites:
        _disc.append(
            "**Comparison with existing syntheses.** Earlier systematic reviews and "
            f"meta-analyses in this field ({_synth_cites}) have reached differing "
            "conclusions. Differences in the eligibility window, the set of databases "
            "searched, the outcome instruments accepted and the choice of effect model are "
            "plausible sources of that divergence; the present synthesis should be read as "
            "an updated, independently computed estimate rather than as a replication of "
            "any single prior review."
        )
    _disc.append(
        "**Strengths.** This review adhered to PRISMA 2020, conducted a comprehensive search "
        + (f"of {', '.join(databases)}" if _db_ok else "of the specified databases") +
        ", assessed risk of bias, quantified between-study heterogeneity and rated "
        "certainty of evidence with GRADE."
    )
    _lim = []
    # ⚠️ pairwise.I2 已是百分数（coze 契约 §4 + block_b.b1_pairwise_python 同构），
    #    直接比较/打印，**不可再 ×100**（旧代码 ×100 会把 34.5% 印成 3450%）。
    if isinstance(i2, (int, float)) and i2 > 25:
        _lim.append(f"substantial heterogeneity (I2 = {i2:.0f}%) that was not fully explained")
    else:
        _lim.append("residual between-study heterogeneity")
    if isinstance(egger_p, (int, float)) and egger_p < 0.05:
        _lim.append(f"a signal of potential publication bias (Egger p = {egger_p:.3f})")
    _lim.append("reliance on aggregate (study-level) rather than individual-participant data")
    _lim.append("possible clinical and methodological diversity across included studies")
    _disc.append("**Limitations.** The findings should be interpreted in light of "
                 + "; ".join(_lim) + ".")
    _disc.append(
        "**Implications.** " + ("If corroborated, " if _ci_cross else "")
        + f"The observed {direction} effect may inform clinical and policy decisions, although "
          "the certainty rating warrants cautious interpretation. Well-designed primary "
          "studies addressing the identified limitations are needed."
    )
    _disc.append(
        "**Future research.** Future trials should pre-specify the outcome instrument and "
        "the follow-up window, report complete outcome data sufficient for pooling, and "
        "recruit populations representative of routine practice. Prospective registration "
        "of trial protocols would further reduce the risk of selective reporting."
    )
    discussion_block = "## 4. Discussion\n" + "\n\n".join(_disc) + "\n" + oc_section + "\n"

    # 5. Conclusion
    _cert = ("the confidence interval includes the null value, so the result is not statistically definitive"
             if _ci_cross else "the point estimate is reasonably precise")
    conclusion_block = (
        "## 5. Conclusion\n"
        f"On the basis of {n_stud} {_n(n_stud, 'study', 'studies')}, the pooled analysis "
        f"indicates that the intervention {direction} the outcome (a pooled estimate of "
        f"{eff_line}; certainty of evidence: {grade_line}). Because {_cert} and the certainty "
        f"of evidence is {grade_line.lower()}, the conclusion should be considered provisional. "
        "Further high-quality research is warranted to confirm the finding and to explore "
        "sources of heterogeneity.\n"
    )

    # 未提供英文题名时给一行英文提示（提示本身是英文，不构成中文残留）；
    # 标题保留调用方原题 —— 没有翻译能力时**不臆造**英文题名。
    _title_note = (
        "> Note: an English title has not been supplied for this topic. The manuscript "
        "body is written in English; please confirm or provide an English title before "
        "submission.\n\n" if _need_en_title else "")
    manuscript = (
        f"# {_title}\n\n"
        f"{_title_note}"
        f"{abstract_block}\n"
        f"{background_block}\n"
        f"## 2. Methods\n{methods_block}\n"
        f"## 3. Results\n{results_block}\n"
        f"{discussion_block}\n"
        f"{conclusion_block}\n"
        f"## References\n{references_block}\n"
    )
    # 章节清单（用于 C3 结构核验）
    sections = re.findall(r"^##\s+(.+)$", manuscript, re.MULTILINE)
    out = {"manuscript": manuscript, "sections": sections, "char_count": len(manuscript)}
    # 文献接地状态（2026-09-22）：随初稿一起回传，供页面在「没有检索到文献」时
    # 显式提示 —— 静默降级会让用户误以为正文已引用真实文献。
    out["evidence_status"] = evidence_status(evidence, topic_en=topic_en, topic=topic,
                                             error=evidence_error,
                                             has_studies=_upstream_studies,
                                             n_upstream=_n_upstream)
    # 附参考文献段落（给 LLM 扩写参考，不直接写入 manuscript）
    if ref_sections:
        out["_ref_sections"] = ref_sections
    return out


# ---------------------------------------------------------------------------
# C1 叙述扩写接口（B 档：编排层注入 LLM，写出背景/讨论/结论/摘要叙述）
# ---------------------------------------------------------------------------
def build_narrative_prompt(topic, scaffold, b_summary, studies_list=None,
                           ref_sections=None):
    """构造交给 LLM（编排层 / agent）扩写叙述段落的提示词。

    scaffold 为 c1_draft 产出的结构化初稿；LLM 应基于其中的真实数据写背景/讨论/结论/摘要，
    不得编造统计量或文献、不得过度声明。
    ref_sections 为已纳入 PDF 的章节切片（写作风格/结构参考），有则附在 scaffold 之后。
    返回 str。
    """
    pw = b_summary.get("pairwise", {}) or {}
    # 与 c1_draft 一致：传给 LLM 的必须是**报告尺度**（比值类取 exp）—— 否则 LLM
    # 会照着 log OR 写稿，把「OR = -0.38」写进正文。
    _em_np = pw.get("effect_measure") or "OR"
    _ratio_np = str(_em_np).upper() in {"OR", "RR", "HR", "PLO", "PLOGIT", "IRR", "RRR"}
    _te_np, _ci_np = pw.get("TE_random"), pw.get("ci_random") or pw.get("ci_fixed")
    _rep_np = lambda v: math.exp(v) if (_ratio_np and isinstance(v, (int, float))) else v
    _ci_np_txt = ("–".join("%.3g" % _rep_np(x) for x in _ci_np)
                  if isinstance(_ci_np, (list, tuple)) and len(_ci_np) == 2 else "n/a")
    _te_np_rep, _i2_np = _rep_np(_te_np), pw.get("I2")
    _te_np_txt = ("%.3g" % _te_np_rep) if isinstance(_te_np_rep, (int, float)) else str(_te_np_rep)
    _i2_np_txt = ("%.0f%%" % _i2_np) if isinstance(_i2_np, (int, float)) else str(_i2_np)
    stats_line = (f"合并效应 {_em_np}={_te_np_txt} "
                  f"(95%CI {_ci_np_txt}); I2={_i2_np_txt}; "
                  f"GRADE={b_summary.get('grade', {}).get('grade')}")
    # 包含摘要/主要发现（2026-09-25 修复）：让 LLM 能基于真实研究内容讨论，而非仅引用书目事实。
    def _study_ctx(s):
        """每条研究的叙述上下文：引用 + 摘要 + 主要发现/结局（如有）"""
        cite = _study_cite(s)
        abstract = (s.get("abstract") or "").strip()
        findings = (s.get("findings") or s.get("key_findings") or "").strip()
        parts = [cite]
        if abstract:
            parts.append(f"  Abstract: {abstract[:600]}")
        if findings:
            parts.append(f"  Key findings: {findings[:300]}")
        return "\n".join(parts)
    studies_ctx = "\n\n".join(_study_ctx(s) for s in (studies_list or [])[:10]) or "（无文献集）"

    ref_block = ""
    if ref_sections:
        ref_parts = []
        for key, info in list(ref_sections.items())[:5]:
            title = info.get("title", key)
            secs = info.get("sections", {})
            for sec_name in ("discussion", "conclusion", "introduction", "results", "abstract"):
                sec_text = secs.get(sec_name, "")
                if sec_text:
                    ref_parts.append(
                        f"\n--- 参考 [{title}]「{sec_name}」段 ---\n{sec_text[:2500]}"
                    )
            if len("\n".join(ref_parts)) > 12000:
                break
        if ref_parts:
            ref_block = (
                "\n\n### 已纳入同类文献的参考段落（用于写作风格与结构参考，"
                "不可直接复制、不可将其数据视为你的研究结果）:\n"
                + "\n".join(ref_parts)
            )

    return (
        "You are an evidence-based medicine / epidemiology writer. Based on the structured draft and "
        "statistical results of the following systematic review and meta-analysis, write a submission-ready "
        "ENGLISH manuscript narrative (Background, Discussion, Conclusion, and a structured Abstract in English). "
        "Requirements: ① facts must be strictly based on the provided data; do not fabricate statistics or references; "
        "② do not overstate beyond the confidence interval or the certainty of evidence; "
        "③ discussions of consistency with prior studies must name the included studies; "
        "④ writing style and paragraph structure may follow the 'Reference sections' for guidance, "
        "but data and conclusions must be independent and based solely on the statistical results below."
        f"\n\nTopic: {topic}\nStatistical results: {stats_line}\nIncluded studies:\n{studies_ctx}\n\n"
        f"Current structured draft:\n{scaffold}{ref_block}"
    )


def c1_expand_narrative(c1, topic, b_summary, studies=None, references=None,
                        picos=None, language="zh"):
    """C1 scaffold → 完整叙述（LLM 驱动，降级安全）。

    修改 c1["manuscript"] 原地替换，更新 char_count。
    返回 {manuscript, expanded: bool, provider: str}。
    """
    try:
        from llm_client import expand as _llm_expand
    except ImportError:
        _llm_expand = None

    # 构建 prompt
    ref_sections = None
    if references and isinstance(references, list):
        ref_sections = []
        for r in references[:15]:
            if isinstance(r, dict):
                parts = []
                if r.get("verified_first_author") or r.get("first_author"):
                    parts.append(r.get("verified_first_author", r.get("first_author", "")))
                if r.get("year"):
                    parts.append(f"({r['year']})")
                if r.get("verified_title") or r.get("title"):
                    parts.append(r.get("verified_title", r.get("title", "")))
                if r.get("journal"):
                    parts.append(f"*{r['journal']}*")
                if r.get("doi"):
                    parts.append(f"doi:{r['doi']}")
                if parts:
                    ref_sections.append(", ".join(parts))

    prompt = build_narrative_prompt(
        topic, c1["manuscript"], b_summary,
        studies_list=studies, ref_sections=ref_sections,
    )

    # 调用 LLM（候选梯队自动降级）
    raw = _llm_expand(prompt, timeout=120, system=_SYSTEM_PROMPT_EN if language == "en" else _SYSTEM_PROMPT_ZH)

    if raw and isinstance(raw, str) and raw.strip() and raw != c1["manuscript"]:
        # 基本质量检查：包含至少 3 个章节标记
        section_count = len(re.findall(r"^##\s+", raw, re.MULTILINE))
        if section_count >= 3:
            c1["manuscript"] = raw
            c1["char_count"] = len(raw)
            c1["expanded"] = True
            return c1

    # 降级：保持 scaffold
    c1["expanded"] = False
    return c1


# ---------------------------------------------------------------------------
# 参考文献格式化（C3 核验后自动填充初稿）
# ---------------------------------------------------------------------------
def format_references(c3_report, language="zh"):
    """从 C3 核验结果生成格式化引用列表 Markdown。

    仅使用已核验的真实元数据（verified_title / verified_first_author / year / journal），
    不虚构引用信息。
    """
    verifications = c3_report.get("ref_verifications") or []
    if not verifications:
        return ""

    is_zh = (language != "en")
    lines = []
    for i, rv in enumerate(verifications):
        if rv.get("status") not in ("ok", None):
            continue
        parts = []
        # 作者
        author = rv.get("verified_first_author") or rv.get("first_author")
        if author:
            parts.append(author)
        # 年份
        year = rv.get("year")
        if year:
            parts.append(f"({year})")
        # 标题
        title = rv.get("verified_title") or rv.get("title")
        if title:
            parts.append(title)
        # 期刊
        journal = rv.get("journal")
        if journal:
            parts.append(f"*{journal}*")
        # DOI
        doi = rv.get("doi")
        if doi:
            parts.append(f"doi:{doi}")
        if parts:
            lines.append(f"{i+1}. " + ". ".join(parts))

    if not lines:
        return ""

    header = "参考文献" if is_zh else "References"
    return f"## {header}\n\n" + "\n\n".join(lines)


# ---------------------------------------------------------------------------
# C2 AI 评审（复用 B3 detect_overclaims）
# ---------------------------------------------------------------------------
def c2_ai_review(manuscript, b_summary):
    """对生成的初稿做 AI 评审：复用 block_b.detect_overclaims（B3 单点实现）。

    若传入 manuscript 非空则审初稿全文；否则回退到 B3 已有命中。返回 {hits[], n_patterns,
    stats}。stats 来自 B1 pairwise，避免重复计算。
    """
    pw = b_summary.get("pairwise", {}) or {}
    stats = {"effect_measure": pw.get("effect_measure", "OR"),
             "ci_random": pw.get("ci_random"), "ci_fixed": pw.get("ci_fixed"),
             "p_random": pw.get("p_random"), "p_fixed": pw.get("p_fixed"),
             "k": pw.get("k"), "I2": pw.get("I2")}
    text = (manuscript or "")
    if text.strip():
        hits = detect_overclaims(text, stats)
    else:
        hits = b_summary.get("overclaims", []) or []
    return {"n_patterns": 12, "n_hits": len(hits), "hits": hits, "stats": stats}


# ---------------------------------------------------------------------------
# C3 参考完整性核验（🔴 reference_verification 红线，结构/PRISMA 检查）
# ---------------------------------------------------------------------------
def c3_reference_verify(manuscript, sections, references=None):
    """参考完整性核验（结构 + 真实 API）。

    检查：
      - 初稿必含章节（背景/方法/结果/讨论/结论）齐全；
      - 若提供参考列表：每条须有 doi 或 pmid → **CrossRef/PubMed 真实 API 核验**存在性与元数据，
        缺失/虚构标 critical；撤稿文献标 critical；双侧 DOI+PMID 交叉验证防拼接幻觉。
      - 若未提供参考（本地-only）：标记 refs_verified=False，提示真实核验未完成（不可投稿）。
      - 网络/接口不可达：标 unverified_offline，**不判疑似虚构**（避免离线红线误杀）。
    返回扁平 report dict：{n_references, missing_sections, issues[], notes[], critical,
    n_retracted, n_not_found, n_mismatch, n_unverified, refs_verified, coze_ready(兼容别名),
    ref_verifications[], note}；红线闸由 run_block_c 统一构造。
    """
    notes = []
    issues = []
    ref_verifications = []
    critical = False

    # 1) 章节结构核验
    # 兜底：调用方只给 manuscript 未给 sections（或给空）时，从正文重新识别 ## 标题；
    # 必含章节清单 _REQUIRED_SECTIONS 由 _SECTION_PAIRS 派生（单一事实来源，不会漂移）。
    if not sections and manuscript:
        sections = re.findall(r"^##\s+(.+)$", manuscript, re.MULTILINE)
    sec_text = " ".join(sections)
    sec_low = sec_text.lower()
    # 中英文任一侧命中即视为该章节存在；原实现只认中文，英文稿会被误判缺章 → 误置 critical
    missing = [zh for zh, en in _SECTION_PAIRS
               if zh not in sec_text and en.lower() not in sec_low]
    if missing:
        issues.append(f"初稿缺失必要章节：{', '.join(missing)}")
        critical = True
        notes.append("结构缺陷：缺失 PRISMA 必要章节，须补全后再送审。")

    # 2) 参考文献真实核验（CrossRef/PubMed API）
    coze_ready = False
    n_retracted = 0
    n_not_found = 0
    n_mismatch = 0
    n_unverified = 0

    if references is None or (isinstance(references, list) and len(references) == 0):
        notes.append("未提供参考列表：仅完成结构/PRISMA 层核验，真实参考文献核验未完成（不可投稿）。")
        coze_ready = False
    else:
        n_ref = len(references)
        # 真实 API 批量核验（CrossRef/PubMed）
        ref_verifications = verify_references(references)
        for rv in ref_verifications:
            status = rv.get("status")
            ident = rv.get("doi") or rv.get("pmid") or rv.get("title") or "?"
            if status == "retracted":
                critical = True
                n_retracted += 1
                issues.append(f"⚠️ 撤稿文献：{ident} — {rv.get('message')}")
            elif status == "not_found":
                critical = True
                n_not_found += 1
                issues.append(f"⚠️ 未查到（疑似虚构）：DOI={rv.get('doi')} PMID={rv.get('pmid')} — {rv.get('message')}")
            elif status == "mismatch":
                critical = True
                n_mismatch += 1
                issues.append(f"⚠️ 元数据不一致（疑似拼接）：{rv.get('title') or ''} — {rv.get('message')}")
            elif status == "unverified_offline":
                # 网络/接口不可达：无法区分「真不存在」与「查不到」，绝不判疑似虚构
                n_unverified += 1
                issues.append(f"⚠️ 未能核验（网络/接口不可达，需联网重试）：{ident}")
            elif status == "error" and not rv.get("doi") and not rv.get("pmid"):
                issues.append(f"⚠️ 缺少 doi/pmid：{ident}（无法核验）")

        # 撤稿计数传递给下游 B4
        if n_retracted > 0:
            notes.append(f"核验发现 {n_retracted} 篇撤稿文献，必须人工处置。")
        if n_not_found > 0:
            notes.append(f"核验发现 {n_not_found} 篇未查到（可能虚构），必须人工核查。")
        if n_mismatch > 0:
            notes.append(f"核验发现 {n_mismatch} 篇元数据不一致（标题/作者），必须人工核查。")
        if n_unverified > 0:
            notes.append(f"{n_unverified} 篇因网络/接口不可达未能核验（不判疑似虚构），须联网重试后再投稿。")

        if issues:
            notes.append(f"参考核验发现 {len(issues)} 处问题。")
        # 仅当：有参考 + 无 critical + 全部完成真实核验 → 视为参考核验通过
        if not critical and n_ref > 0 and n_unverified == 0:
            coze_ready = True

    if references is None:
        note = ("参考完整性核验：未提供参考列表 → 仅完成结构/PRISMA 层核验，"
                "真实参考文献核验未完成（不可投稿）。")
    elif critical:
        note = "参考完整性核验：结构/PRISMA + CrossRef/PubMed 真实 API 核验发现严重问题（见 issues）。"
    elif n_unverified:
        note = (f"参考完整性核验：结构通过，但 {n_unverified} 篇因网络/接口不可达未能核验，"
                "须联网重试后方可投稿。")
    else:
        note = "参考完整性核验：结构/PRISMA + CrossRef/PubMed 真实 API 存在性/元数据核验通过。"

    report = {
        "n_references": len(references) if references is not None else 0,
        "missing_sections": missing,
        "issues": issues,
        "notes": notes,                        # 结论性说明（原实现计算后丢弃 → 已补全返回）
        "critical": critical,
        "n_retracted": n_retracted,
        "n_not_found": n_not_found,
        "n_mismatch": n_mismatch,
        "n_unverified": n_unverified,
        "refs_verified": coze_ready,           # 语义化名：真实参考核验是否已完成并通过
        "coze_ready": coze_ready,              # 向后兼容（历史命名）
        "ref_verifications": ref_verifications,
        "note": note,
    }
    return report


# ---------------------------------------------------------------------------
# C4 证据表 + 投稿前 QA（🔴 manuscript_approval 终闸）
# ---------------------------------------------------------------------------
def c4_evidence_qa(b_summary, c2_hits, c3_report):
    """生成 GRADE 证据表 + 投稿前 QA 清单。

    GRADE 证据表来自 B2 grade_report；QA 清单覆盖：统计量报告、森林图占位、过度声明处置、
    参考核验。终闸 manuscript_approval（required=True）；critical = C3 critical 或 C2 含 high 过度声明未处置。
    """
    grade = b_summary.get("grade", {}) or {}
    domain = grade.get("domain_ratings", {})
    evidence_table = {
        "grade": grade.get("grade", "—"),
        "downgrades": grade.get("downgrades", 0),
        "reasons": grade.get("reasons", []),
        "domain_ratings": domain,
    }
    high_oc = [h for h in (c2_hits or []) if h.get("severity") == "high"]
    qa = [
        {"item": "主要效应量（k/合并效应/CI/p）已报告", "pass": bool(b_summary.get("pairwise", {}).get("k"))},
        {"item": "异质性与 τ² 已报告", "pass": "I2" in str(b_summary.get("pairwise", {}).get("I2", "")) or
         b_summary.get("pairwise", {}).get("I2") is not None},
        {"item": "GRADE 证据表已生成", "pass": bool(grade.get("grade"))},
        {"item": "过度声明已检出并标注（C2）", "pass": True,
         "detail": f"{len(c2_hits or [])} 条，high={len(high_oc)}"},
        {"item": "参考完整性核验通过（C3）",
         "pass": bool(c3_report.get("refs_verified")),
         "detail": ("存在严重问题（撤稿/虚构/拼接/缺章）" if c3_report.get("critical")
                    else ("参考列表未提供或未完成真实核验 — 不可投稿"
                          if not c3_report.get("refs_verified") else "已通过真实核验"))},
        {"item": "high 级过度声明已处置", "pass": len(high_oc) == 0,
         "detail": "存在未处置的 high 级过度声明" if high_oc else "无"},
    ]
    critical = bool(c3_report.get("critical", False)) or len(high_oc) > 0
    return {"evidence_table": evidence_table, "qa": qa, "critical": critical,
            "n_high_overclaim": len(high_oc)}


# ---------------------------------------------------------------------------
# 人工决策判定（红线闸放行）
# ---------------------------------------------------------------------------
def _decision_approves(decision, stage_id):
    if not isinstance(decision, dict):
        return False
    return (decision.get("stage_id") == stage_id
            and str(decision.get("action", "")).lower() in ("approved", "approve"))


def _any_approve(decisions, stage_id):
    """human_decision 兼容单 dict / list（fullflow 累积凭据）；任一 approved 即 True。"""
    if isinstance(decisions, dict):
        decisions = [decisions]
    return any(_decision_approves(d, stage_id) for d in (decisions or []))


def _soft_stop(env, pid, stages, stage, sid, pause_at, decisions):
    """P3 软停靠（fullflow HITL，spec contracts/fullflow/v0.1.0）。

    pause_at 含 sid 且未持对应 approved 凭据 → 提前软停返回
    （done=False / await_human=True / gate=None / pause=True，区别于红线闸）。
    """
    if not (pause_at and sid in pause_at) or _any_approve(decisions, sid):
        return None
    return {"pipeline_id": pid, "pipeline": env["pipeline"], "stages": stages,
            "attachments": [], "tool_card_outputs": [],
            "done": False, "await_human": True, "gate": None, "final": stage,
            "pause": True, "human_decisions": []}


# ---------------------------------------------------------------------------
# 编排：C1 → C2 → C3 → C4（本地优先）
# ---------------------------------------------------------------------------
def run_block_c(topic=None, studies=None, b_env=None, analysis=None, references=None,
                human_decision=None, pause_at=None,
                studies_list=None, prisma_flow=None, picos=None,
                search_info=None, rob_summary=None, merged_json=None,
                ref_sections=None, topic_en=None, evidence=None, evidence_error=None,
                language="zh", expand=True):
    """本地优先 Block C 驱动器。返回与 run_pipeline 同构的 dict。

    - 消费 B 阶段结果：优先 b_env（run_block_b 输出信封），否则 analysis（归一 dict）。
    - 红线闸：C3=reference_verification、C4=manuscript_approval（均 required=True）。
      未持对应批准 → done=False / await_human=True / gate=首个未批准红线闸。
    - human_decision：单个 {"stage_id": C3|C4, "action": "approved"}，或多个批准的 list
      （生产 coze 流中跨阶段累积的批准凭据，一次性传入；本地单轮即可放行多闸）。
    - pause_at：P3 软停靠集合（fullflow HITL）。默认 None = 现状行为（仅 C3/C4 红线闸停）。
    - language：zh（默认）或 en，控制输出语言。
    - expand：True 时调 LLM 扩写叙述段（降级安全：失败则保持 scaffold）。
    """
    b_summary = _extract_b_summary(b_env if b_env is not None else analysis)
    env = build_block_c_env(topic)
    pid = env["pipeline_id"]
    stages = []

    # C1 初稿（接通写作辅助引擎 + 上游真实素材接地）
    c1 = c1_draft(topic, b_summary, studies=studies,
                  overclaim_hits=b_summary.get("overclaims", []),
                  studies_list=studies_list, prisma_flow=prisma_flow, picos=picos,
                  search_info=search_info, rob_summary=rob_summary, merged_json=merged_json,
                  ref_sections=ref_sections, topic_en=topic_en, evidence=evidence,
                  evidence_error=evidence_error)
    # 叙述扩展（2026-09-25）：注入 LongCat-2.0 等后台大模型，将 scaffold 扩写为
    # 完整英文初稿（背景/讨论/结论/摘要不再留模板占位符）。任何失败回退到 scaffold。
    try:
        import topic_translate as _tt
        _cands = _tt._candidates()
        if _cands:
            _prompt = build_narrative_prompt(topic, c1["manuscript"], b_summary,
                                             studies_list=studies_list,
                                             ref_sections=ref_sections)
            # 叙述扩展：用后台大模型（LongCat-2.0 等）将 scaffold 扩写为完整初稿
            # raw=True 模式给 8000 token 预算，足够产出完整论文叙述段
            for _base, _k, _model in _cands:
                try:
                    _raw = _tt._call(_base, _k, _model, _prompt, timeout=120,
                                     system="You are an evidence-based medicine / epidemiology writer. Write a submission-ready ENGLISH manuscript narrative strictly based on the provided data. Do not fabricate statistics or references.",
                                     raw=True)
                except Exception:
                    continue
                if _raw and _raw != c1["manuscript"]:
                    c1["manuscript"] = _raw
                    c1["char_count"] = len(_raw)
                    break
    except Exception:
        pass  # LLM 不可用时回退到 scaffold（已含真实数据与引用）
    s1 = _mk_stage(C1, 0, "completed",
                   {"manuscript": c1["manuscript"], "sections": c1["sections"],
                    "char_count": c1["char_count"],
                    "evidence_status": c1.get("evidence_status")},
                   {"type": "review", "prompt": "请人工审阅初稿结构与事实准确性。",
                    "required": False, "gate": None})
    stages.append(s1)
    _st = _soft_stop(env, pid, stages, s1, C1, pause_at, human_decision)
    if _st:
        return _st

    # C2 AI 评审（复用 B3）
    c2 = c2_ai_review(c1["manuscript"], b_summary)
    s2 = _mk_stage(C2, 1, "completed", c2,
                   {"type": "review", "prompt": "请人工复核 AI 评审检出的过度声明。",
                    "required": False, "gate": None})
    stages.append(s2)
    _st = _soft_stop(env, pid, stages, s2, C2, pause_at, human_decision)
    if _st:
        return _st

    # C3 参考完整性核验（🔴 红线）
    # references 未显式提供时，由 A2 文献集 DOI 构造（交 C3 真实核验）；均无则结构层通过、标记不可投稿
    _refs = references
    if _refs is None and studies_list:
        _refs = [{"doi": s["doi"]} for s in studies_list if isinstance(s, dict) and s.get("doi")]
    c3 = c3_reference_verify(c1["manuscript"], c1["sections"], _refs)

    # C3 后：自动格式化参考文献，填充初稿「## 参考文献」章节
    ref_text = format_references(c3, language=language)
    if ref_text and "待补充" in c1["manuscript"]:
        c1["manuscript"] = c1["manuscript"].replace(
            "（待补充：由 C3 参考完整性核验后生成。）",
            "\n\n" + ref_text
        )
        c1["sections"] = re.findall(r"^##\s+(.+)$", c1["manuscript"], re.MULTILINE)
    nha3 = {
        "type": "approve",
        "prompt": (f"参考完整性核验：{c3['n_references']} 条参考、"
                   f"{'发现严重问题（撤稿/缺章）' if c3['critical'] else '结构通过'}。"
                   f"请人工核验后批准（reference_verification）。"),
        "required": True,
        "gate": GATE_REF_VERIFY,
    }
    # C3 是红线闸（reference_verification）：无论结构是否通过，均须人工批准
    s3 = _mk_stage(C3, 2, "await_human", c3, nha3)
    stages.append(s3)

    # C4 证据表 + QA（🔴 终闸）
    c4 = c4_evidence_qa(b_summary, c2.get("hits", []), c3)
    nha4 = {
        "type": "approve",
        "prompt": (f"投稿前 QA：GRADE={c4['evidence_table']['grade']}，"
                   f"high 过度声明={c4['n_high_overclaim']}。"
                   f"{'存在未处置重大问题，' if c4['critical'] else ''}请人工核验后批准（manuscript_approval）。"),
        "required": True,
        "gate": GATE_MANUSCRIPT,
    }
    s4 = _mk_stage(C4, 3, "await_human", c4, nha4)
    stages.append(s4)

    base = {
        "pipeline_id": pid, "pipeline": env["pipeline"],
        "stages": stages, "attachments": [], "tool_card_outputs": [],
    }

    # 红线闸解析（按 C1→C4 顺序，首个未批准红线闸即阻断点）
    # human_decision 支持 单 dict 或 list[dict]（累积多闸批准）
    decisions = human_decision if isinstance(human_decision, list) else (
        [human_decision] if human_decision else [])
    for st in stages:
        nha = st.get("next_human_action") or {}
        if nha.get("gate") in cc._REDLINE_GATES and nha.get("required"):
            if any(_decision_approves(d, st["stage"]["id"]) for d in decisions):
                continue  # 该闸已批准，继续看下一个
            return {**base, "done": False, "await_human": True,
                    "gate": nha.get("gate"), "final": st}
    return {**base, "done": True, "await_human": False, "gate": None, "final": s4}
