#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""flow_menu.py -- CCM (Conversation Context Menu) 对话上下文菜单渲染器。

定位
----
工作台（adapters/workbench/）已有完整的 11 节点渲染契约（form_schema）与 HITL
状态机（fullflow），但**对话侧没有菜单**：每轮展示什么、闸位有哪些选项，全靠 LLM
即兴，同一节点两次渲染可能不一致。本模块给同一套 schema 加一层「对话投影」，
**不新建第二套流程定义**。

硬约束（违反即视为实现缺陷，见 references/conversation_flow_menu.md §1）
--------------------------------------------------------------------
R1  状态真源只有一个：复用 fullflow_session_ff-*.json，本模块**只读**（除 decide/rewind）。
R2  菜单由代码产出、LLM 只转述——渲染必须确定性，同输入同输出。
R3  🔴 选项由 cc._REDLINE_GATES 派生过滤，**不硬编码第二份清单**。
R4  可编辑键由 fullflow.EDITABLE_KEYS 派生，**不自行声明**（未收录的修订项显式标注为不可用）。
R5  当前节点由 cursor / 信封派生；回退候选集从信封 stage 序列派生
    （与 workbench server.build_state 同源，**不重写 workbench.html 的 JS 逻辑**）。
R6  纯算数请求不出现 CCM（本模块不被调用即为满足）。

用法
----
    python flow_menu.py status  [--session P] [--lang zh|en] [--json]
    python flow_menu.py menu    [--session P] [--lang zh|en] [--json]
    python flow_menu.py nodes   [--lang zh|en] [--json]
    python flow_menu.py decide  [--session P] --option N [--revision '<json>'|--set k=v]
                                [--note S] [--apply]
    python flow_menu.py rewind  [--session P] --target A2.literature_search [--apply]
    python flow_menu.py probe   [--session P] [--lang zh|en] [--max N] [--apply]

`decide` / `rewind` 默认是 **dry-run**（只校验不落盘）；加 `--apply` 才真正推进
（会重跑块，可能触网）。校验一律走 fullflow._validate_decision —— 不在本层复述规则。

退出码：0 成功；2 用法/校验错误；3 会话缺失或不可解析。
"""

import argparse
import datetime
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(_HERE)
_ADAPTERS = os.path.join(_SKILL_ROOT, "adapters")
_WORKBENCH = os.path.join(_ADAPTERS, "workbench")

# 入径顺序：adapters/ 使其能 import fullflow / coze_client；workbench/ 使其能 import form_schema。
for _p in (_ADAPTERS, _WORKBENCH, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import form_schema  # noqa: E402  （纯数据，无外部依赖）
import fullflow  # noqa: E402
import coze_client as cc  # noqa: E402

DEFAULT_RUNS_DIR = os.path.join(_WORKBENCH, "runs")

# A 阶段四节点 + 出口闸（本模块当前覆盖范围；B/C 节点走同一套投影，见 nodes）
# 合并节点（用户裁定 2026-09-10）：原「检索」+「初筛」= 单节点「文献集」。
A_STAGES = ("A1.topic_selection", "A2.literature_search", "A3.pdf_download", "A4.data_extraction")

# 节点短名（en）。zh 短名直接取 form_schema.STAGE_ORDER 第三列（单一真源）。
_EN_SHORT = {
    "A1.topic_selection": "Topic",
    "A2.literature_search": "LitSet",
    "A3.pdf_download": "PDF",
    "A4.data_extraction": "Extract",
    # 2026-09-22（一致性审计 P0-1）：键必须是真实 stage id（block_b.B1 = "B1.meta_analysis"），
    # 此前写作 "B1.meta" → EN 模式下该节点短名回落中文，且与 form_schema 的漂移同源。
    "B1.meta_analysis": "Meta",
    "B2.grade": "GRADE",
    "B3.overclaim": "Overclaim",
    "B4.quality_gate": "Quality",
    "C1.draft": "Draft",
    "C2.ai_review": "AIReview",
    "C3.ref_verify": "RefCheck",
    "C4.evidence_qa": "QA",
}

# 数据源显示名（advisory）：仅用于 A2「沉默漏检」提示，运行时优先从
# ct-literature 的 _SOURCE_DISPLAY 读取（单一真源），读不到才用本常量。
# 见 tests/test_flow_menu.py::test_expected_sources_in_sync。
_FALLBACK_SOURCES = ("OpenAlex", "EuropePMC", "bioRxiv", "medRxiv",
                     "SemanticScholar", "arXiv")


class MenuError(Exception):
    """会话缺失 / 无法解析 / 校验失败。"""


# ---------------------------------------------------------------------------
# i18n（自包含：不改动 ct-base 共享的 i18n_messages.json）
# ---------------------------------------------------------------------------
_T = {
    "hdr":           {"zh": "## 当前流程设定 / Current pipeline settings:",
                      "en": "## Current pipeline settings / 当前流程设定:"},
    "nav":           {"zh": "全流程", "en": "Pipeline"},
    "soft":          {"zh": "软停 · 需你拍板", "en": "soft pause · needs your call"},
    "redline":       {"zh": "🔴 红线 · 必须你放行", "en": "🔴 redline · your approval required"},
    "handoff":       {"zh": "块间交接确认", "en": "Block handoff"},
    "handoff_tag":   {"zh": "交接闸 · 仅批准/打回", "en": "handoff · approve/reject only"},
    "done":          {"zh": "全流程已完成", "en": "pipeline finished"},
    "no_session":    {"zh": "未找到会话文件", "en": "no session file found"},
    "none":          {"zh": "（无）", "en": "(none)"},
    "topic":         {"zh": "选题", "en": "Topic"},
    "missing":       {"zh": "缺失维度", "en": "missing dimensions"},
    "probe":         {"zh": "注册库探针", "en": "registry probe"},
    "scope":         {"zh": "检索范围", "en": "search scope"},
    "scope_orig":    {"zh": "仅原始研究（= 源头排除综述）", "en": "primary research only (reviews excluded at source)"},
    "scope_rev":     {"zh": "含综述类文献（伞评/范围综述）", "en": "include reviews (umbrella/scoping)"},
    "merged":        {"zh": "合并", "en": "merged"},
    "status":        {"zh": "状态", "en": "status"},
    "limit":         {"zh": "检索上限", "en": "max results"},
    "per_source":    {"zh": "/源（合并上限 = 源数 × 上限）", "en": "/source (merged cap = sources × limit)"},
    "raw_topic":     {"zh": "原始主题", "en": "raw topic"},
    "query":         {"zh": "优化检索式", "en": "optimized query"},
    "untranslated":  {"zh": "未翻译残留", "en": "untranslated left"},
    "retracted":     {"zh": "撤稿", "en": "retracted"},
    "dedup":         {"zh": "去重", "en": "deduped"},
    "rule_inc":      {"zh": "规则纳入", "en": "rule include"},
    "rule_exc":      {"zh": "规则剔除", "en": "rule exclude"},
    "uncertain":     {"zh": "低置信", "en": "low-confidence"},
    "type_dist":     {"zh": "类型（规则预填）", "en": "doc type (rule-prefilled)"},
    "type_confirm":  {"zh": "类型确认", "en": "doc type confirmed"},
    "rule_src":      {"zh": "规则来源", "en": "rule source"},
    "rule_src_v":    {"zh": "ct-literature PRISMA 确定性初筛 + classify_record（均已预填进导出表）",
                      "en": "ct-literature PRISMA deterministic pre-screen + classify_record (both pre-filled in the export)"},
    "file_io":       {"zh": "导出合并表", "en": "export merged table"},
    "file_io_v":     {"zh": "改「裁决」「理由」「文献类型确认」三列 → [4] 传回，即接 ③",
                      "en": "edit the Decision / Reason / Doc-type columns → [4] upload back to reach ③"},
    "screened":      {"zh": "初筛通过", "en": "screened in"},
    "downloaded":    {"zh": "已下载全文", "en": "full texts fetched"},
    "extracted":     {"zh": "已抽取", "en": "extracted"},
    "pending_pdf":   {"zh": "待补传 PDF", "en": "PDF to supply"},
    "pending_pdf_v": {"zh": " 篇（非 OA / 付费墙）→ 影响纳入量，请处置",
                      "en": " (non-OA / paywalled) → affects inclusion, please handle"},
    "type_readonly": {"zh": "类型（只读 A2 确认值）", "en": "doc type (read-only, from A2)"},
    "pdf_hint":      {"zh": "首次进入：若手头已有部分文献的 PDF，请直接发送其所在文件夹（或文件）路径——将优先用本地 PDF 抽取，减少付费墙漏检；没有可回「跳过本提示」。",
                      "en": "First entry: if you already have some PDFs locally, send the folder (or file) path(s) -- local PDFs are extracted first, reducing paywalled misses; reply 'skip' to omit."},
    "pdf_dir_set":   {"zh": "已登记本地 PDF 路径：",
                      "en": "Registered local PDF path: "},
    "gate_dist":      {"zh": "门控分布", "en": "gate distribution"},
    "litset":        {"zh": "文献集（检索 + 初筛）", "en": "Literature set (search + screening)"},
    "opt_export":    {"zh": "导出合并表", "en": "Export merged table"},
    "opt_import":    {"zh": "传回修改后的合并表", "en": "Upload modified merged table"},
    "opt_approve_export": {"zh": "批准并下载 PDF", "en": "Approve & download PDFs"},
    "opt_export_check":   {"zh": "导出检查（不改变状态）", "en": "Export for review (no state change)"},
    "opt_probe":     {"zh": "先帮我选题（可行性速览）", "en": "Feasibility quick view"},
    "opt_probe_v":   {"zh": "跑一次注册库探针，先看拥挤度/证据量再放行 ②", "en": "one registry probe to gauge crowding/evidence before approving ②"},
    "a1_need_topic":  {"zh": "请先输入选题（含 PICOS 更佳）——直接发主题文字即可。选题确认后菜单才会给出「批准 / 改 PICOS / 改检索范围 / 可行性速览」选项，再进入 ② 文献集；② 批准即下载 PDF 进入 ③ 数据抽取，如需修改合并表可导出检查后用 [4] 传回修改后的合并表。",
                       "en": "Enter a topic first (PICOS preferred) -- just send the topic text. Once the topic is set, the menu will show the 'Approve / Edit PICOS / Toggle review inclusion / Feasibility quick view' options before proceeding to ② literature set; approving ② downloads PDFs and enters ③ data extraction -- edit the exported table offline and use [4] Upload modified merged table to send it back."},
    "handoff_p":     {"zh": "块 %s 完成，即将进入 %s。请确认交接数据。",
                      "en": "Block %s done, entering %s. Please confirm the handoff."},
    "handoff_d":     {"zh": "待交接研究", "en": "studies to hand off"},
    "no_skip":       {"zh": "⚠️ 本节点无「跳过」——红线闸不接受 skipped",
                      "en": "⚠️ no Skip here -- redline gates reject skipped"},
    "blocked":       {"zh": "暂不可用", "en": "unavailable"},
    "blocked_why":   {"zh": "EDITABLE_KEYS 未收录该键，修改不会传播到下游",
                      "en": "key not in EDITABLE_KEYS; the edit would not reach downstream"},
    "src_missing":   {"zh": "沉默漏检", "en": "silent omission"},
    "src_missing_v": {"zh": "未返回结果的库", "en": "sources returning nothing"},
    "src_empty":     {"zh": "沉默漏检：本次检索未返回任何结果（检查 token / skill / 网络）",
                      "en": "silent omission: search returned nothing (check tokens / skill / network)"},
    "src_single":    {"zh": "沉默漏检：仅 %s 一个库返回结果，其余库可能被静默跳过",
                      "en": "silent omission: only %s returned results; other sources may have been silently skipped"},
    "search_bad":    {"zh": "检索状态 ≠ ok，结果可能不完整/为空", "en": "search_status != ok; results may be incomplete/empty"},
    "untrans_warn":  {"zh": "检索式含未翻译词，建议补全或换英文主题", "en": "query contains untranslated terms; complete them or use an English topic"},
    "audit":         {"zh": "审计", "en": "audit"},
    "already":       {"zh": "已决策", "en": "decided"},
    "dryrun":        {"zh": "DRY-RUN（未落盘）", "en": "DRY-RUN (nothing written)"},
    "applied":       {"zh": "已落盘", "en": "applied"},
    "rewind_to":     {"zh": "回退到", "en": "rewind to"},
    "opt_approve":   {"zh": "批准", "en": "Approve"},
    "opt_revise":    {"zh": "修订", "en": "Revise"},
    "opt_skip":      {"zh": "跳过", "en": "Skip"},
    "opt_reject":    {"zh": "打回", "en": "Reject"},
}


def _lang(code=None):
    if code in ("zh", "en"):
        return code
    try:
        import i18n
        return "zh" if i18n.is_chinese_os() else "en"
    except Exception:  # noqa: BLE001
        return "en"


def L(key, lang, *args):
    """取本地化文案；args 非空时做 % 插值。"""
    e = _T.get(key) or {}
    v = e.get(lang)
    if v is None:
        v = e.get("en")
    if v is None:
        v = key
    return (v % args) if args else v


# ---------------------------------------------------------------------------
# 会话发现 / 装载
# ---------------------------------------------------------------------------
def list_sessions(runs_dir=None):
    """runs 目录下全部会话路径（按 updated_at 倒序，最新在前）。"""
    d = runs_dir or DEFAULT_RUNS_DIR
    if not os.path.isdir(d):
        return []
    out = []
    for fn in os.listdir(d):
        if fn.startswith("fullflow_session_") and fn.endswith(".json"):
            out.append(os.path.join(d, fn))
    def _key(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f).get("updated_at") or ""
        except Exception:  # noqa: BLE001
            return ""
    return sorted(out, key=_key, reverse=True)


def resolve_session(path=None, runs_dir=None):
    """显式路径优先；否则取最新会话。返回 (sess, path)。"""
    if path:
        p = os.path.abspath(os.path.expanduser(path))
        if not os.path.isfile(p):
            raise MenuError(f"会话文件不存在：{p}")
    else:
        cands = list_sessions(runs_dir)
        if not cands:
            raise MenuError(L("no_session", "en") + f" @ {runs_dir or DEFAULT_RUNS_DIR}")
        p = cands[0]
    return fullflow.FullflowSession.load(p), p


# ---------------------------------------------------------------------------
# 状态派生（只读；与 workbench.server.build_state 同源同轴）
# ---------------------------------------------------------------------------
#: 键 → CLI 修订项文案（修订项由 EDITABLE_KEYS 派生，见 _fallback_options）。
#: 未列出的键用通用文案 —— 宁可朴素也不漏项。
_KEY_LABEL = {
    "report":         {"zh": "修订报告正文", "en": "Edit report"},
    "include_reviews": {"zh": "改「纳入综述」开关", "en": "Toggle include-reviews"},
    "sources":        {"zh": "改检索数据源", "en": "Edit data sources"},
    "query":          {"zh": "改检索式", "en": "Edit query"},
    "screened":       {"zh": "传回修改后的裁决表", "en": "Import revised screening"},
    "pdf_dir":        {"zh": "登记本地 PDF 目录", "en": "Set local PDF dir"},
    "extracted_rows": {"zh": "修订 2×2 表", "en": "Edit 2x2 tables"},
    "pairwise":       {"zh": "修订合并结果 pairwise", "en": "Edit pooled result"},
    "nma":            {"zh": "修订 NMA 结果", "en": "Edit NMA result"},
    "manuscript":     {"zh": "修订正文", "en": "Edit manuscript"},
    "sections":       {"zh": "修订章节清单", "en": "Edit section list"},
}


def _stage_entries(sess):
    """信封 stage 序列（块序 + 块内序），与 server.build_state 的 progress 同序。"""
    rows = []
    for b in ("A", "B", "C"):
        env = ((sess.data.get("blocks") or {}).get(b) or {}).get("envelope")
        if not env:
            continue
        for i, st in enumerate(env.get("stages") or []):
            rows.append({"block": b, "index": i,
                         "stage_id": (st.get("stage") or {}).get("id"),
                         "status": st.get("status"), "stage": st})
    return rows


def resolve_await(sess):
    """当前等待态。真源 = last_view.fullflow.await；缺失则从信封/cursor 兜底。"""
    lv = (sess.data.get("last_view") or {}).get("fullflow") or {}
    aw = dict(lv.get("await") or {})
    if aw.get("kind"):
        return aw, lv
    cur = sess.data.get("cursor") or {}
    for row in reversed(_stage_entries(sess)):
        if row["status"] == "await_human" and row["stage_id"]:
            sid = row["stage_id"]
            return {"kind": "gate" if _gate_of(sid) else "pause",
                    "gate": _gate_of(sid), "stage_id": sid}, lv
    return {"kind": cur.get("await_kind") or "done", "stage_id": cur.get("stage_id")}, lv


def _gate_of(sid):
    """stage_id → gate 名（若为红线闸）。真源 = fullflow.STAGE_TO_GATE ∩ cc._REDLINE_GATES。"""
    g = fullflow.STAGE_TO_GATE.get(sid)
    return g if g in cc._REDLINE_GATES else None


def is_redline(sid):
    return _gate_of(sid) is not None


def machine_options(sess, aw=None):
    """该停靠点的合法 action 集（**由状态机派生，不硬编码**）。

    与 fullflow._view() 同口径：红线闸 → approved/revised/rejected（拒 skip）；
    软停 → + skipped；交接闸 → approved/rejected。
    """
    aw = aw if aw is not None else resolve_await(sess)[0]
    kind = aw.get("kind")
    if kind == "handoff_confirm":
        return ["approved", "rejected"]
    if kind == "done":
        return []
    sid = aw.get("stage_id")
    if is_redline(sid):
        return ["approved", "revised", "rejected"]
    if kind == "pause":
        return ["approved", "revised", "skipped", "rejected"]
    return aw.get("options") or ["approved", "revised", "rejected"]


def build_progress(sess):
    """11 节点 → 状态（done / current / pending）。线性轴，早期节点由决策审计兜底。"""
    aw, _ = resolve_await(sess)
    kind = aw.get("kind")
    cur_sid = aw.get("stage_id")
    decided = {d.get("stage_id") for d in (sess.data.get("human_decisions") or [])
               if d.get("action") in ("approved", "revised", "skipped")}
    ent = {}
    for row in _stage_entries(sess):
        if row["stage_id"]:
            ent[row["stage_id"]] = row["status"]
    order = [sid for _b, sid, _lab in form_schema.STAGE_ORDER]
    idx = {sid: i for i, sid in enumerate(order)}
    cur_i = idx.get(cur_sid)
    out = {}
    for sid in order:
        if kind == "done":
            out[sid] = "done"
            continue
        if sid == cur_sid and kind in ("gate", "pause"):
            out[sid] = "current"
            continue
        # 下游节点一律未达：即使信封里出现（构造/重放场景）也不得标 ✓
        if cur_i is not None and idx[sid] > cur_i:
            out[sid] = "pending"
            continue
        seen = sid in ent or sid in decided
        if seen and (sid in decided or ent.get(sid) in ("completed", "done")):
            out[sid] = "done"
        elif seen and cur_i is not None and idx[sid] < cur_i:
            out[sid] = "done"
        else:
            out[sid] = "pending"
    return out


# ---------------------------------------------------------------------------
# 选项集（节点专属语义）—— 一切 decision 选项都会被 machine_options 过滤
# ---------------------------------------------------------------------------
_A1_TOPIC_PLACEHOLDERS = ("新课题", "待设定", "待输入", "未填写", "请输入")


def _a1_topic_missing(sr, sess):
    """A1 初始态判定：无选题（空 or 占位符）→ 菜单须显式提示用户输入。"""
    t = str(_a1_topic(sr, sess) or "").strip()
    if not t:
        return True
    return any(p in t for p in _A1_TOPIC_PLACEHOLDERS)


def _a1_summary(sess, sr, nha, aw, lang):
    lines = []
    if _a1_topic_missing(sr, sess):
        lines.append(("hint", L("a1_need_topic", lang)))
    else:
        lines.append(("topic", _a1_topic(sr, sess)))
    picos = sr.get("picos") or {}
    picos = dict(picos)
    lines.append(("picos", " ｜ ".join(
        f"{k} {picos.get(k) or '-'}" for k in ("P", "I", "C", "O", "S"))))
    miss = sr.get("missing_dimensions") or []
    if miss:
        lines.append(("missing", " · ".join(miss)))
    probe = sr.get("registry_probe") or {}
    if probe:
        tot = probe.get("total")
        fea = sr.get("feasibility") or {}
        crowd = fea.get("crowding")
        bits = [f"{probe.get('status')}"]
        if tot is not None:
            bits.append(("相关试验 %s 项" % tot) if lang == "zh" else (f"{tot} trials"))
        if crowd and crowd != "unknown":
            bits.append(("拥挤度 %s" % crowd) if lang == "zh" else (f"crowding {crowd}"))
        lines.append(("probe", " → ".join(str(b) for b in bits)))
    _scope_mode = L("scope_rev" if sr.get("include_reviews") else "scope_orig", lang)
    import block_a  # 延迟导入：避免启动时拉起整个块层
    _srcs = sr.get("sources") or list(block_a.CORE_SOURCES)
    _src_str = "、".join(str(s) for s in _srcs) if _srcs else L("none", lang)
    lines.append(("scope", f"{_scope_mode} ｜ 数据源：{_src_str}"))
    return lines


def _a2_summary(sess, sr, nha, aw, lang):
    """合并节点摘要（2026-09-10）：检索覆盖（原 A2）+ 初筛漏斗（原 A3），一张表两段。

    `cov` 缺席时不渲染检索段（旧会话停在已并入 A2 的独立 A3 节点时如此），避免
    打印 ``合并 None ｜ 状态 None``——菜单也不该出现 None（AC-A9）。
    """
    cov = (nha.get("coverage") or sr.get("coverage") or {})
    summ = nha.get("summary") or {}
    lines = []
    if cov:
        by = cov.get("by_source") or {}
        src = " · ".join(f"{k} {v}" for k, v in sorted(by.items())) or L("none", lang)
        head = [f"{L('merged', lang)} {cov.get('total')}",
                f"{L('status', lang)} {cov.get('search_status')}", src]
        lines.append(("cov", " ｜ ".join(head)))
        mr = cov.get("max_results")
        lines.append(("limit", f"{mr}{L('per_source', lang)}"))
        lines.append(("raw_topic", str(cov.get("raw_topic") or "")))
        lines.append(("query", str(cov.get("translated_query") or cov.get("query") or "")))
        if cov.get("retracted"):
            lines.append(("retracted", str(cov.get("retracted"))))
        lines.append(("untranslated", ", ".join(cov.get("untranslated") or []) or L("none", lang)))
    # ---- 初筛段（原 A3 摘要，已并入本节点）----
    if summ:
        lines.append(("funnel", f"{L('dedup', lang)} {summ.get('n_total')} ｜ "
                                f"{L('rule_inc', lang)} {summ.get('n_include')} ｜ "
                                f"{L('rule_exc', lang)} {summ.get('n_exclude')} ｜ "
                                f"{L('uncertain', lang)} {summ.get('n_uncertain')}"))
        dist = summ.get("doc_type_dist") or {}
        if dist:
            M = _doc_type_labels(lang)
            lines.append(("type_dist", " · ".join(
                f"{M.get(k, k)} {v}" for k, v in sorted(dist.items(), key=lambda kv: -kv[1]))))
        lines.append(("file_io", L("file_io_v", lang)))
    return lines


#: A2 告警判定口径（用户裁定 2026-09-10）：**只看核心二源**。
#: 与 adapters/block_a.py::CORE_SOURCES 必须一致（tests/test_flow_menu.py 有同步断言）。
CORE_SOURCES = ("OpenAlex", "EuropePMC")


def _a2_discrepancy(sess, sr, nha, aw, lang):
    """A2 存在的理由：暴露沉默漏检——但只对**核心二源**负责。

    用户裁定（2026-09-10）：只要 OpenAlex + EuropePMC 正常返回数据即可，
    其余源（bioRxiv / arXiv / Semantic Scholar 无 key 跳过等）**不再告警**。

      D1  核心源缺位（OpenAlex/EuropePMC 有任一为 0/缺失） → 报
      D2  by_source 为空 / total == 0                      → 确定性空结果，报
      D3  search_status != ok                              → 报（已由核心源口径派生）
      D4  调用方显式给了 --expected-sources                → 差集比对，**仅核心源**生效
    """
    warnings = []
    cov = (nha.get("coverage") or sr.get("coverage") or {})
    if not cov:
        # 无检索覆盖数据（旧会话停在已并入 A2 的独立 A3 节点）→ 无从判定漏检，
        # 不报空结果假警；由 _LEGACY_SESSION_NOTE 说明来龙去脉。
        return warnings
    stt = cov.get("search_status")
    by = cov.get("by_source") or {}
    total = cov.get("total")
    core_missing = [s for s in CORE_SOURCES if not by.get(s)]
    if not by or total in (0, None):
        warnings.append(L("src_empty", lang) if lang == "zh"
                        else L("src_empty", "en"))
    elif core_missing:
        warnings.append(f"{L('src_missing', lang)}：{L('src_missing_v', lang)} "
                        f"{', '.join(core_missing)}")
    if stt and stt != "ok":
        warnings.append(f"{L('search_bad', lang)}（{stt}）")
    exp = current_expected_sources()
    if exp:
        # 仅核心源参与差集：非核心源（bioRxiv/arXiv/…）缺失属常态，不告警。
        missing = [s for s in exp if s in CORE_SOURCES and s not in by]
        if missing:
            warnings.append(f"{L('src_missing', lang)}：{L('src_missing_v', lang)} {', '.join(missing)}")
    if cov.get("untranslated"):
        warnings.append(L("untrans_warn", lang))
    return warnings


def _a4_summary(sess, sr, nha, aw, lang):
    lines = []
    rows = sr.get("extracted_rows") or sr.get("extracted_rows_review") or []
    lines.append(("funnel", f"{L('screened', lang)} {sr.get('n_screened')} ｜ "
                            f"{L('downloaded', lang)} {sr.get('n_downloaded')} ｜ "
                            f"{L('extracted', lang)} {sr.get('n_extracted')}（2×2 {len(rows)}）"))
    up = sr.get("needs_user_upload") or []
    if up:
        lines.append(("pending_pdf", f"{len(up)}" + L("pending_pdf_v", lang)))
    per = sr.get("per_doc") or []
    if per:
        dist = {}
        for d in per:
            if isinstance(d, dict) and d.get("doc_type"):
                dist[d["doc_type"]] = dist.get(d["doc_type"], 0) + 1
        if dist:
            M = _doc_type_labels(lang)
            lines.append(("type_readonly", " · ".join(
                f"{M.get(k, k)} {v}" for k, v in sorted(dist.items(), key=lambda kv: -kv[1]))))
    # D19：把 fetch_log 的 gate 分布摊开，避免「已下载 0」掩盖配额挡 / 抽取失败等沉默漏检。
    fl = sr.get("fetch_log") or []
    if fl:
        gdist = {}
        for e in fl:
            if isinstance(e, dict) and e.get("gate"):
                gdist[e["gate"]] = gdist.get(e["gate"], 0) + 1
        blockers = {g: c for g, c in gdist.items() if not g.startswith("pass_")}
        if blockers:
            GL = _fetch_gate_labels(lang)
            lines.append(("gate_dist", " · ".join(
                f"{GL.get(g, g)} {c}" for g, c in sorted(blockers.items(), key=lambda kv: -kv[1]))))
    # 首次出现提示（2026-09-11 用户裁定）：A4 菜单首次出现时要求用户提供本地
    # PDF 所在路径。路径经 A4 修订键 pdf_dir 登记（EDITABLE_KEYS），_run_block
    # 注入 run_block_a(pdf_dir=…) → auto_fetch_dir，优先消费本地 PDF 抽取。
    # 已登记则展示路径值替代提示；未登记（含 rewind 重入）持续提示直至批准离开。
    rev4 = sess.latest_revision("A4.data_extraction") or {}
    pdf_dir = rev4.get("pdf_dir")
    if pdf_dir:
        lines.append(("hint", L("pdf_dir_set", lang) + str(pdf_dir)))
    else:
        lines.append(("hint", L("pdf_hint", lang)))
    return lines


def _a3_summary(sess, sr, nha, aw, lang):
    lines = []
    lines.append(("funnel", f"{L('screened', lang)} {sr.get('n_screened')} ｜ "
                            f"{L('downloaded', lang)} {sr.get('n_downloaded')} ｜ "
                            f"{L('pending_pdf', lang).split('（')[0]} {sr.get('n_pending', 0)}"))
    rev3 = sess.latest_revision("A3.pdf_download") or {}
    pdf_dir = rev3.get("pdf_dir")
    if pdf_dir:
        lines.append(("hint", L("pdf_dir_set", lang) + str(pdf_dir)))
    else:
        lines.append(("hint", L("pdf_hint", lang)))
    return lines


def _a3_options(lang):
    return [
        {"n": 1, "kind": "decision", "action": "approved",
         "label": L("opt_approve_export", lang)},
        {"n": 2, "kind": "revise", "key": "pdf_dir",
         "label": ("指定本地 PDF 路径" if lang == "zh" else "Set local PDF path")},
        {"n": 3, "kind": "revise", "key": "extracted_rows",
         "label": L("opt_import", lang)},
        {"n": 4, "kind": "rewind", "target": "A2.literature_search",
         "label": ("回退 ② 文献集" if lang == "zh" else "Rewind to ② literature set")},
    ]


def _fetch_gate_labels(lang):
    """A4 fetch_log 各 gate 的展示标签（D19）。pass_* 为成功态，不在 blocker 分布里。"""
    zh = {
        "relevance_skip": "A2 裁决排除", "quota_deferred": "配额暂缓",
        "no_local_pdf": "本地无 PDF", "no_candidate": "无 DOI/PMID",
        "pass_no_oa": "非 OA/付费墙", "pass_download_fail": "下载失败",
        "extract_fail": "抽取失败", "worker_error": "处理异常", "failed": "失败",
    }
    en = {
        "relevance_skip": "excluded by A2 screening", "quota_deferred": "quota deferred",
        "no_local_pdf": "no local PDF", "no_candidate": "no DOI/PMID",
        "pass_no_oa": "paywalled / non-OA", "pass_download_fail": "download failed",
        "extract_fail": "extract failed", "worker_error": "worker error", "failed": "failed",
    }
    return zh if lang == "zh" else en


def _a1_topic(sr, sess):
    """A1 的选题标题：优先报告里的 `**选题**：` 行，其次会话 topic，最后首行非空。"""
    rep = str(sr.get("report") or "")
    parts = rep.splitlines()
    for ln in parts:
        t = ln.strip()
        if t.startswith("**选题**"):
            v = t.split("：", 1)[-1].split(":", 1)[-1].strip()
            if v:
                return v
    if rep and len(parts) <= 1 and not rep.startswith("#"):
        return rep.strip()
    for ln in parts:
        t = ln.strip().lstrip("#").strip()
        if t and not t.startswith("|"):
            return t
    return str(sess.data.get("topic") or "")


def _a1_stage_result(sess):
    """返回信封里 A1 节点的 stage_result 可变引用（不存在则回 None）。"""
    for row in _stage_entries(sess):
        if row["stage_id"] == "A1.topic_selection":
            return (row["stage"] or {}).setdefault("stage_result", {})
    return None


def a1_feasibility_probe(sess, max_results=10):
    """选题阶段「可行性速览」：跑一次注册库探针，把结果写回 A1 stage_result
    的 ``registry_probe`` / ``feasibility``，使 A1 摘要实时反映拥挤度与风险预警。

    复用 ``block_a.a1_topic_selection`` 的 feasibility 阈值计算（只取 registry_probe +
    feasibility 两字段，**不覆盖**用户已改的 report 文本）。无有效选题时拒绝
    （需先输入选题）。registry_probe 缺失/异常时优雅降级（status=error 仍落盘，
    由 _a1_warnings 暴露）。
    """
    sr = _a1_stage_result(sess)
    if sr is None:
        raise MenuError("本会话信封无 A1 节点，无法做可行性速览。")
    topic = (_a1_topic(sr, sess) or sess.data.get("topic") or "").strip()
    if not topic or _a1_topic_missing(sr, sess):
        raise MenuError("A1 尚无有效选题，无法做可行性速览；请先输入选题"
                        "（直接发主题文字，或用 [2] 改 PICOS 报告）。")
    try:
        import block_a  # 延迟导入：避免启动时拉起整个块层
    except Exception as e:  # noqa: BLE001
        raise MenuError(f"无法加载 block_a（可行性速览依赖）：{type(e).__name__}: {e}")
    probe = block_a.a1_registry_check(topic, max_results=max_results)
    # 仅取 registry_probe + feasibility（feasibility 阈值计算复用 block_a 单一真源）
    # 2026-09-25：PROSPERO 手动核查链接须用英文检索词，优先取 session 中已翻译的 topic_en
    topic_en = sr.get("topic_en") or sess.data.get("topic_en") or None
    rep, _ = block_a.a1_topic_selection(topic, registry_probe=probe, topic_en=topic_en)
    sr["registry_probe"] = rep.get("registry_probe", probe)
    sr["feasibility"] = rep.get("feasibility",
                                {"crowding": "unknown", "expected_studies": None,
                                 "risk_alert": None})
    # 2026-09-25：同步写回 topic_analysis（含临床价值 LLM 评估结果），
    # 使速览面板能展示临床维度评分与依据，而非仅显示「需人工确认」。
    if rep.get("topic_analysis"):
        sr["topic_analysis"] = rep["topic_analysis"]
    sess.save()
    return probe


def _a1_options(lang):
    # A1 收敛为「批准 / 修订」两态：不提供 info 展开、不提供 skip、不提供 reject。
    # 注：machine_options 仍由状态机派生（软停语义含 skipped），此处只是菜单窄化展示。
    return [
        {"n": 1, "kind": "decision", "action": "approved", "label": L("opt_approve", lang)},
        {"n": 2, "kind": "revise", "key": "report",
         "label": ("改 PICOS 报告" if lang == "zh" else "Edit PICOS report")},
        {"n": 3, "kind": "revise", "key": "include_reviews",
         "keys": ["include_reviews", "sources"], "toggle": True,
         "label": ("改检索范围（综述 + 数据源）" if lang == "zh"
                   else "Edit retrieval scope (reviews + sources)"),
         "note": ("含/排除综述类，并增减本次检索的数据源（如 OpenAlex、EuropePMC、PubMed…）；"
                  "当前数据源见上方「检索范围」行。" if lang == "zh"
                 else "Toggle review inclusion and adjust the screened data sources "
                      "(e.g. OpenAlex, EuropePMC, PubMed…); current sources on the scope line above.")},
        # 可行性速览（2026-09-11 新增）：选题阶段即可按需触发注册库探针，
        # 不跑整条检索管线，先看拥挤度/证据量再决定要不要放行 ②。
        # 非状态机决策项，由 agent 调 `flow_menu.py probe --apply` 落地
        # （见 a1_feasibility_probe，把 registry_probe/feasibility 写回 A1 stage_result）。
        # 选题缺失时由 build_menu 自动隐藏（与 hint 同语义：先输入选题）。
        # 注：用户 2026-09-11 两次裁定——「上传裁决表」先移出 A1（只留 A2），
        # 随后 A2 的「传回合并表」也移除（[4] 撤销）：离线修改后直接走
        # ③ 数据抽取（A4）修订。A1 仅承载选题批准 / 修订 / 可行性速览。
        {"n": 4, "kind": "probe", "what": "feasibility",
         "label": L("opt_probe", lang)},
    ]


def _a2_options(lang):
    # 用户裁定（2026-09-10）：A2 检索 与 A3 初筛**合并为单节点「文献集」** →
    # 一个软停、一张合并表。
    # 用户裁定（2026-09-11 两轮）：[1] 改「批准并下载 PDF」（批准触发 A4 自动落盘，
    # 本地 pdf_dir 优先）；[3] 明示仅供检查（file/export，agent 侧动作，非决策项）；
    # [4] 恢复为「传回修改后的合并表」= revise/screened（接缝修复：EDITABLE_KEYS
    # 本就收录 screened，改用 revise 项后传回可走标准 decide 通路，而非仅菜单展示）。
    # 同 A1：菜单窄化展示，machine_options 仍由状态机按软停语义派生。
    return [
        {"n": 1, "kind": "decision", "action": "approved",
         "label": L("opt_approve_export", lang)},
        {"n": 2, "kind": "revise", "key": "query",
         "label": ("改检索式" if lang == "zh" else "Edit query")},
        {"n": 3, "kind": "file", "what": "export", "label": L("opt_export_check", lang)},
        {"n": 4, "kind": "revise", "key": "screened",
         "label": L("opt_import", lang),
         "note": ("上传修改后的合并表（Excel/CSV），识别「裁决」列按逐条裁决解析，"
                  "无裁决列视为文献清单整表替换；解析结果写入 screened 后重跑下游。"
                  if lang == "zh"
                  else "Upload the modified merged table (Excel/CSV); a Decision column "
                       "is parsed row-by-row, otherwise the list replaces the set; "
                       "parsed rows go to `screened` and downstream reruns.")},
    ]


def _a4_options(lang):
    # 无「跳过」：红线闸不接受 skipped（由 machine_options 兜底过滤）。
    return [
        {"n": 1, "kind": "decision", "action": "approved",
         "label": ("批准（放行 → Block B）" if lang == "zh" else "Approve (→ Block B)")},
        {"n": 2, "kind": "upload", "what": "pdf",
         "label": ("上传补 PDF" if lang == "zh" else "Supply missing PDFs")},
        {"n": 3, "kind": "revise", "key": "extracted_rows",
         "label": ("修订 2×2 表" if lang == "zh" else "Edit 2x2 tables")},
        {"n": 4, "kind": "rewind", "target": "A2.literature_search",
         "label": ("回退 ② 文献集" if lang == "zh" else "Rewind to ② literature set")},
        {"n": 5, "kind": "decision", "action": "rejected", "label": L("opt_reject", lang)},
    ]


def _handoff_options(lang):
    return [
        {"n": 1, "kind": "decision", "action": "approved",
         "label": ("批准进入下一块" if lang == "zh" else "Approve, enter next block")},
        {"n": 2, "kind": "decision", "action": "rejected", "label": L("opt_reject", lang)},
    ]


_OPTION_BUILDERS = {
    "A1.topic_selection": _a1_options,
    "A2.literature_search": _a2_options,
    "A3.pdf_download": _a3_options,
    "A4.data_extraction": _a4_options,
}

_SUMMARY_BUILDERS = {
    "A1.topic_selection": _a1_summary,
    "A2.literature_search": _a2_summary,
    "A3.pdf_download": _a3_summary,
    "A4.data_extraction": _a4_summary,
}

_WARN_BUILDERS = {
    "A2.literature_search": _a2_discrepancy,
}


def _fallback_options(sess, aw, lang):
    """无节点专属 builder 时的基础兜底菜单（冲突3(b) 修复）。

    仅生成状态机合法的基础 decision 项，让 B4/C1/C3/C4 等无专属 builder 的停靠点
    **不再渲染空选项菜单**（原实现 ob=None → out["options"] 恒为 []，红线/软停闸位
    在对话侧只见「必须你放行」却无 [批准/打回] 可点）：
      - 红线闸 → machine_options 返回 [approved, revised, rejected] → 给 [批准, 打回]
      - 软停   → 返回 [approved, revised, skipped, rejected]       → 给 [批准, 跳过, 打回]
    revised 不在此生成（B/C 节点未实现字段级修订入口，规范 §scope 明确细节后续按需补），
    避免用户选了「修订」却无字段可改。选项仍经 `_filter_options` 二次过滤，与 R3/R4 同源。
    """
    allowed = machine_options(sess, aw)
    out, n = [], 1
    if "approved" in allowed:
        out.append({"n": n, "kind": "decision", "action": "approved",
                    "label": L("opt_approve", lang)})
        n += 1
    # 2026-09-22（一致性审计 P1-6）：此前此处**不生成 revised**（原理由：B/C 节点未实现
    # 字段级修订入口）。但网页侧 B4「完整质量报告」与 C1「正文」早有 editable 面板可改后
    # 重新提交 → 对话侧却选不到「修订」，两侧不对等。现改为**从单一真源
    # fullflow.EDITABLE_KEYS 派生**：该阶段声明了哪些可修订键，就产出对应修订项；
    # 声明为空（B2/C2/C3/C4 —— 其键或不存在、或无人消费）则如实不提供。
    if "revised" in allowed:
        for k in fullflow.EDITABLE_KEYS.get(aw.get("stage_id") or "", []):
            lb = _KEY_LABEL.get(k) or {}
            out.append({"n": n, "kind": "revise", "key": k,
                        "label": lb.get(lang) or lb.get("en") or
                                 (("修订 %s" % k) if lang == "zh" else ("Edit %s" % k))})
            n += 1
    if "skipped" in allowed:
        out.append({"n": n, "kind": "decision", "action": "skipped",
                    "label": L("opt_skip", lang)})
        n += 1
    if "rejected" in allowed:
        out.append({"n": n, "kind": "decision", "action": "rejected",
                    "label": L("opt_reject", lang)})
        n += 1
    return out


# 对话侧标题覆盖（**仅当工作台与对话侧的节点语义真实不同时才允许**，且必须写明理由）：
# A2 合并节点 —— 对话侧零逐条编辑入口（D9：整节点塌成「导出合并表 / 传回」文件交接），
# 故标题点明"检索 + 初筛"两件事，避免与工作台 rowlist 口径混同。
_CCM_TITLE_OVERRIDE = {
    "A2.literature_search": {"zh": "文献集 · 检索 + 初筛（一张表）",
                             "en": "Literature set · search + screening (one table)"},
}

# 旧会话兼容（2026-09-10 A2/A3 合并）：合并前会话的游标可能停在独立 `A3.screening` 节点。
# 该节点在新 schema 中已无定义——直接用原 sid 渲染会得到一个**空菜单**（标题是裸 id、
# 正文与选项皆空），既不诚实也不可用。这里把**渲染**投影到合并节点 A2（摘要/选项/标题），
# 但**决策仍走真实 sid**（state machine 侧 `_run_block` 已能消费旧 A3 载荷）。
# 由此用户既能看到真实数据（漏斗 + 类型分布 + 文件交接），又不会被伪装成"当前契约"。
_LEGACY_SID_ALIAS = {"A3.screening": "A2.literature_search"}

_LEGACY_SESSION_NOTE = {
    "zh": "本会话创建于 A2/A3 合并之前，游标停在已并入 ② 的独立「A3 初筛」节点；"
          "下面按合并后的 ② 文献集投影展示。批准后 A4 将沿用本会话已算好的裁决清单。",
    "en": "This session predates the A2/A3 merge; its cursor sits on the standalone "
          "'A3 screening' node now folded into ②. Rendered here as the merged ② "
          "literature set. Approving runs A4 with the decision list already in this session.",
}


def _ccm_title(sid, lang):
    # 旧会话兼容：已并入 A2 的独立 A3 节点按合并节点标题渲染（见 _LEGACY_SID_ALIAS）
    sid = _LEGACY_SID_ALIAS.get(sid, sid)
    ov = _CCM_TITLE_OVERRIDE.get(sid)
    if ov:
        return ov.get(lang) or ov.get("en")
    return form_schema.title_for(sid, lang)


def _a1_warnings(sess, sr, nha, aw, lang):
    w = []
    fea = sr.get("feasibility") or {}
    if fea.get("risk_alert"):
        w.append(str(fea["risk_alert"]).strip().lstrip("⚠️").strip())
    rep = str(sr.get("report") or "")
    if "缺失维度过多" in rep and not fea.get("risk_alert"):
        w.append("PICOS 缺失维度过多，建议先明确研究问题。" if lang == "zh"
                 else "Too many missing PICOS dimensions; clarify the question first.")
    probe = sr.get("registry_probe") or {}
    if probe.get("status") in ("error", "failed"):
        w.append(("注册库探针异常：%s" % (probe.get("note") or probe.get("status"))) if lang == "zh"
                 else ("Registry probe failed: %s" % (probe.get("note") or probe.get("status"))))
    return w


_WARN_BUILDERS["A1.topic_selection"] = _a1_warnings


def expected_sources(lang=None):
    """ct-literature 可调度源的显示名（**能力清单，不是本次期望**）。

    单一真源 = ct-literature `adapters/fetch_coze_unified._SOURCE_DISPLAY`；
    运行时优先从该模块读取（模块不可用则回退 `_FALLBACK_SOURCES`，并保留同步测试）。
    仅用于 `--expected-sources` 的候选展示与测试同步，**不作为缺库判据**。
    """
    try:
        _ct = cc.resolve_skill_dir("~/.workbuddy/skills/ct-literature")
        p = os.path.join(_ct, "adapters")
        if p not in sys.path:
            sys.path.insert(0, p)
        import fetch_coze_unified as _fcu  # type: ignore
        disp = getattr(_fcu, "_SOURCE_DISPLAY", None)
        if isinstance(disp, dict) and disp:
            return tuple(disp.values())
    except Exception:  # noqa: BLE001
        pass
    return _FALLBACK_SOURCES


# 显式期望源（None = 不比对）。由 CLI --expected-sources 或调用方设置。
_EXPECTED_OVERRIDE = None


def set_expected_sources(names):
    """设置「本次检索应当返回哪些库」。None = 关闭该项检查（默认）。"""
    global _EXPECTED_OVERRIDE
    if names is None:
        _EXPECTED_OVERRIDE = None
    else:
        _EXPECTED_OVERRIDE = [str(x).strip() for x in names if str(x).strip()]


def current_expected_sources():
    return _EXPECTED_OVERRIDE


def _doc_type_labels(lang):
    """文献类型显示标签。单一真源 = block_a.DOC_TYPE_LABELS / _EN（D17-A 的权威词表）。"""
    try:
        import block_a
        return (block_a.DOC_TYPE_LABELS if lang == "zh"
                else block_a.DOC_TYPE_LABELS_EN)
    except Exception:  # noqa: BLE001
        return {}


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------
_CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫"


def _mark(status):
    return {"done": "✓", "current": "▶", "pending": "○"}.get(status, "○")


def render_nav(sess, lang, prog=None):
    """L0 上下文导航条：11 节点压一行（每轮必贴）。"""
    prog = prog or build_progress(sess)
    groups = {}
    for i, (blk, sid, lab) in enumerate(form_schema.STAGE_ORDER):
        short = lab if lang == "zh" else _EN_SHORT.get(sid, lab)
        groups.setdefault(blk, []).append(
            f"{_CIRCLED[i]}{short} {_mark(prog.get(sid))}")
    body = "  │  ".join(f"{b}: " + "  ".join(v) for b, v in groups.items())
    return f"📍 {L('nav', lang)}  │  {body}"


def build_menu(sess, lang="zh"):
    """确定性菜单模型（纯数据，供文本渲染 / JSON 双用）。"""
    aw, lv = resolve_await(sess)
    kind = aw.get("kind")
    sid = aw.get("stage_id")
    prog = build_progress(sess)
    out = {
        "session_path": sess.path,
        "pipeline_id": sess.data.get("pipeline_id"),
        "topic": sess.data.get("topic"),
        "cursor": sess.data.get("cursor"),
        "await": {"kind": kind, "gate": aw.get("gate"), "stage_id": sid,
                  "prompt": aw.get("prompt")},
        "redline": is_redline(sid) if sid else False,
        "machine_options": machine_options(sess, aw),
        "progress": prog,
        "editable_keys": list(fullflow.EDITABLE_KEYS.get(sid or "", [])),
        "nav": render_nav(sess, lang, prog),
        "header": L("hdr", lang),
        "title": None, "tag": None, "lines": [], "warnings": [], "options": [],
        "audit": sess.data.get("human_decisions") or [],
    }
    if kind == "done":
        out["tag"] = L("done", lang)
        return out
    if kind == "handoff_confirm":
        out["title"] = L("handoff", lang)
        out["tag"] = L("handoff_tag", lang)
        hp = lv.get("handoff_preview") or {}
        nxt = hp.get("next") or ""
        pr = {"next": nxt}
        out["lines"] = [("handoff", L("handoff_p", lang, sess.cursor.get("block") or "", nxt))]
        if hp.get("n_studies") is not None:
            out["lines"].append(("studies", f"{L('handoff_d', lang)} {hp['n_studies']}"))
        out["options"] = _filter_options(_handoff_options(lang), sess, aw, sid)
        return out

    st = _stage_entry(sess, sid)
    sr = (st or {}).get("stage_result") or (aw.get("stage_result") or {})
    nha = (st or {}).get("next_human_action") or (aw.get("nha") or {})
    # 渲染投影：旧会话停在已并入 A2 的 A3 节点时，按合并节点 A2 渲染（见 _LEGACY_SID_ALIAS）
    rsid = _LEGACY_SID_ALIAS.get(sid, sid)
    out["title"] = _ccm_title(rsid, lang)
    out["tag"] = L("redline" if out["redline"] else "soft", lang)

    sb = _SUMMARY_BUILDERS.get(rsid)
    if sb:
        out["lines"] = sb(sess, sr, nha, aw, lang)
    wb = _WARN_BUILDERS.get(rsid)
    if wb:
        out["warnings"] = wb(sess, sr, nha, aw, lang)
    if sid in _LEGACY_SID_ALIAS:
        # 显式标注：这是合并前的旧节点投影，不是当前契约
        note = _LEGACY_SESSION_NOTE.get(lang) or _LEGACY_SESSION_NOTE["en"]
        out["warnings"] = [note] + list(out["warnings"])
    ob = _OPTION_BUILDERS.get(rsid)
    if ob:
        opts = ob(lang)
        # 选题缺失时：A1 尚无有效选题，「批准 / 修订 / 可行性速览」均无意义——
        # 只保留 _a1_summary 已加的 hint（提示先输入选题），不渲染任何可操作选项。
        # 用户发主题文字后菜单才重新给出 [1]批准 [2]改PICOS [3]改检索范围 [4]可行性速览。
        if rsid == "A1.topic_selection" and _a1_topic_missing(sr, sess):
            opts = []
        else:
            # 决策仍以真实 sid 过滤（EDITABLE_KEYS 未收录 A3 → 修订项会如实标为不可用）
            out["options"] = _filter_options(opts, sess, aw, sid)
    else:
        # 冲突3(b) 兜底：无节点专属 builder 的停靠点（B4/C1/C3/C4 等）不再渲染空菜单，
        # 按状态机 machine_options 的合法 action 生成 [批准 / 跳过(软停) / 打回] 基础决策菜单，
        # 使红线/软停闸位在对话侧至少可点选推进。revised 不含（B/C 未实现字段级修订入口）。
        out["options"] = _filter_options(_fallback_options(sess, aw, lang), sess, aw, sid)
    return out


def _stage_entry(sess, sid):
    for row in _stage_entries(sess):
        if row["stage_id"] == sid:
            return row["stage"]
    return None


def _filter_options(opts, sess, aw, sid):
    """核心防漂移过滤：decision 选项必须 ⊆ 状态机合法 action 集；
    revise 选项必须 ⊆ EDITABLE_KEYS（未收录则标注不可用，不静默丢弃）。"""
    allowed = set(machine_options(sess, aw))
    editable = set(fullflow.EDITABLE_KEYS.get(sid or "", []))
    out = []
    for o in opts:
        o = dict(o)
        if o["kind"] == "decision":
            if o["action"] not in allowed:
                continue          # 🔴 节点的「跳过」在此被真实状态机挡掉
        elif o["kind"] == "revise":
            if o.get("key") not in editable:
                o["blocked"] = True
                o["blocked_why"] = "EDITABLE_KEYS"
        out.append(o)
    # 重新编号，保证穷举且连续
    for i, o in enumerate(out, 1):
        o["n"] = i
    return out


def render_menu_text(m, lang):
    """把菜单模型渲染成可直接贴给用户的文本（LLM 只转述）。"""
    lines = [m["header"], m["nav"]]
    if m["await"]["kind"] == "done":
        lines.append(f"✅ {m['tag']}")
        return "\n".join(lines)
    S = "：" if lang == "zh" else ": "
    head = m["title"]
    pad = " " * max(2, 46 - _w(head))
    lines.append(f"{head}{pad}〔{m['tag']}〕")
    for w in m["warnings"]:
        lines.append(f"   ⚠️ {w[-1] if isinstance(w, tuple) else w}")
    for k, v in m["lines"]:
        pre = {"topic": "   ", "picos": "   ", "cov": "   ", "dedup": "   ",
               "funnel": "   ", "missing": f"   {L('missing', lang)}{S}",
               "probe": f"   {L('probe', lang)}{S}", "scope": f"   {L('scope', lang)}{S}",
               "limit": f"   {L('limit', lang)}{S}", "raw_topic": f"   {L('raw_topic', lang)}{S}",
               "query": f"   {L('query', lang)}{S}", "untranslated": f"   {L('untranslated', lang)}{S}",
               "retracted": f"   {L('retracted', lang)}{S}",
               "type_dist": f"   {L('type_dist', lang)}{S}",
               "type_confirm": f"   {L('type_confirm', lang)}{S}",
               "rule_src": f"   {L('rule_src', lang)}{S}",
               "pending_pdf": f"   {L('pending_pdf', lang)}{S}",
               "type_readonly": f"   {L('type_readonly', lang)}{S}",
               "gate_dist": f"   {L('gate_dist', lang)}{S}",
               "hint": "   ▸ "}.get(k, "   ")
        if k == "file_io":
            lines.append(f"   ⬇ {L('file_io', lang)} → {v}")
        else:
            lines.append(f"{pre}{v}")
    lines.append("   " + "  ".join(_opt_label(o, lang) for o in m["options"]))
    if m["redline"]:
        lines.append(f"   {L('no_skip', lang)}")
    return "\n".join(lines)


def _opt_label(o, lang):
    lab = o["label"]
    if o.get("blocked"):
        lab = f"{lab}（{L('blocked', lang)}）" if lang == "zh" else f"{lab} ({L('blocked', lang)})"
    return f"[{o['n']}] {lab}"


def _w(s):
    """粗略显示宽度（CJK 记 2）。"""
    return sum(2 if ord(c) > 0x2E7F else 1 for c in s)


# ---------------------------------------------------------------------------
# decide / rewind
# ---------------------------------------------------------------------------
def resolve_option(m, n):
    for o in m["options"]:
        if o["n"] == n:
            return o
    raise MenuError(f"选项 [{n}] 不在本节点选项集内（合法：{ [o['n'] for o in m['options']] }）")


def build_decision(o, revision=None, note=None, stage_id=None):
    d = {"stage_id": stage_id, "action": None, "revision": revision, "note": note,
         "decided_by": "ccm"}
    if o["kind"] == "decision":
        d["action"] = o["action"]
    elif o["kind"] == "revise":
        d["action"] = "revised"
        if revision is None:
            # 单键修订用 o["key"]；多键修订（如选项 3 同时改「综述 + 数据源」）
            # 用 o["keys"] 一次性占位，真实值由 agent 收集后填入。
            _keys = o.get("keys") or [o["key"]]
            d["revision"] = {k: None for k in _keys}
    else:
        raise MenuError(f"选项 [{o['n']}] 不是决策项（kind={o['kind']}），无需 decide")
    return d


def dry_run_validate(sess, decision):
    """唯一校验入口：委托 fullflow._validate_decision（不在本层复述规则）。"""
    return fullflow._validate_decision(sess, decision)


def apply_decision(path, decision, debug=False):
    return fullflow.resume_fullflow(path, decision, debug=debug)


def apply_rewind(path, target, debug=False):
    return fullflow.rewind_fullflow(path, target, debug=debug)


def rewind_candidates(sess):
    """回退候选集：从信封 stage 序列派生（服务端同源），**不重写 workbench.html 的 JS**。"""
    aw, _ = resolve_await(sess)
    cur = aw.get("stage_id")
    order = [sid for _b, sid, _lab in form_schema.STAGE_ORDER]
    # 2026-09-22（一致性审计 P0-1）：此前 `cur not in order → ci = len(order)`，
    # 等于把**全部节点（含尚未到达的下游）**当回退候选 —— 真实误操作风险。
    # 现在优先用**本会话信封的真实序列**（服务端同源，天然只含已发生的阶段），
    # 信封不可用时才回落 STAGE_ORDER；两者都定位不到 cur 则**保守给空集**，
    # 绝不把下游当历史（用户仍可批准 / 打回）。
    ent = [r["stage_id"] for r in _stage_entries(sess) if r["stage_id"]]
    if cur in ent:
        prior = ent[:ent.index(cur)]
    elif cur in order:
        prior = order[:order.index(cur)]
    else:
        return []
    return [sid for sid in prior
            if (form_schema.SCHEMA.get(sid) or {}).get("gate_type") != "auto"]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _parse_set(pairs):
    rev = {}
    for p in pairs or []:
        if "=" not in p:
            raise MenuError(f"--set 需 k=v 形式，收到 {p!r}")
        k, v = p.split("=", 1)
        low = v.strip().lower()
        if low in ("true", "false"):
            rev[k] = (low == "true")
        else:
            rev[k] = v
    return rev


def _print(obj, as_json):
    if as_json:
        print(json.dumps(obj, ensure_ascii=False, indent=2, default=str))
    else:
        print(obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, indent=2))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="flow_menu", description="CCM 对话上下文菜单（A 阶段）")
    ap.add_argument("cmd", choices=["status", "menu", "nodes", "decide", "rewind", "probe"])
    ap.add_argument("--session", "-s", default=None, help="会话文件路径（默认取最新）")
    ap.add_argument("--runs-dir", default=None)
    ap.add_argument("--lang", default=None, choices=["zh", "en"])
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--option", "-o", type=int, default=None, help="decide：选项编号")
    ap.add_argument("--revision", default=None, help="decide：revision JSON 字符串")
    ap.add_argument("--set", action="append", dest="sets", help="decide：单键 k=v（可重复）")
    ap.add_argument("--note", default=None)
    ap.add_argument("--apply", action="store_true", help="decide/rewind：真正落盘并推进")
    ap.add_argument("--target", default=None, help="rewind：目标块字母或 stage_id")
    ap.add_argument("--max", type=int, default=10,
                    help="probe：注册库探针每源样本上限（默认 10）")
    ap.add_argument("--expected-sources", default=None,
                    help="A2：本次检索应当返回的库（逗号分隔），用于缺库比对；不传则不比对")
    ap.add_argument("--debug", action="store_true")
    a = ap.parse_args(argv)
    lang = _lang(a.lang)
    if a.expected_sources is not None:
        set_expected_sources([x for x in a.expected_sources.split(",")])

    try:
        if a.cmd == "nodes":
            rows = []
            for i, (blk, sid, lab) in enumerate(form_schema.STAGE_ORDER):
                sc = form_schema.SCHEMA.get(sid) or {}
                rows.append({"no": _CIRCLED[i], "block": blk, "stage_id": sid,
                             "label": lab if lang == "zh" else _EN_SHORT.get(sid, lab),
                             "gate_type": sc.get("gate_type"),
                             "pausable": sid in fullflow.DEFAULT_PAUSE_AT})
            if a.as_json:
                _print(rows, True)
            else:
                print(L("hdr", lang))
                for r in rows:
                    flag = ("🔴" if r["gate_type"] == "redline"
                            else ("🟡" if r["pausable"] else "  "))
                    print(f"  {r['no']} {r['block']} · {r['stage_id']:24s} {r['label']:12s} {flag}")
            return 0

        sess, path = resolve_session(a.session, a.runs_dir)

        if a.cmd == "status":
            m = build_menu(sess, lang)
            if a.as_json:
                _print({k: m[k] for k in ("session_path", "pipeline_id", "topic",
                                          "cursor", "await", "redline", "progress",
                                          "machine_options", "editable_keys")}, True)
            else:
                _print("\n".join([m["header"], m["nav"]]), False)
            return 0

        if a.cmd == "menu":
            m = build_menu(sess, lang)
            if a.as_json:
                _print(m, True)
            else:
                _print(render_menu_text(m, lang), False)
            return 0

        if a.cmd == "probe":
            # 可行性速览：跑注册库探针 → 写回 A1 stage_result → 重渲染菜单。
            if not a.apply:
                sr = _a1_stage_result(sess) or {}
                topic = (_a1_topic(sr, sess) or sess.data.get("topic") or "")
                _print({"ok": True, "dry_run": True,
                        "topic": topic or "(无选题)",
                        "note": "加 --apply 才真实调 ct-registry 并把结果写回会话 A1.stage_result"},
                       a.as_json)
                return 0
            try:
                probe = a1_feasibility_probe(sess, max_results=a.max)
            except MenuError as e:
                _print({"ok": False, "error": str(e)}, a.as_json)
                return 2
            m = build_menu(sess, lang)
            if a.as_json:
                _print({"ok": True, "applied": True, "probe": probe, "menu": m}, True)
            else:
                _print(render_menu_text(m, lang), False)
            return 0

        if a.cmd == "rewind":
            if not a.target:
                raise MenuError("rewind 需要 --target（块字母或 stage_id）")
            cands = rewind_candidates(sess)
            if a.target not in cands:
                raise MenuError(f"回退目标 {a.target!r} 不是当前节点的上游人工节点；候选：{cands}")
            if not a.apply:
                _print({"dry_run": True, "target": a.target,
                        "candidates": cands}, a.as_json)
                return 0
            res = apply_rewind(path, a.target, debug=a.debug)
            _print({"applied": True, "target": a.target,
                    "await": (res.get("fullflow") or {}).get("await")}, a.as_json)
            return 0

        # decide
        if a.option is None:
            raise MenuError("decide 需要 --option N")
        m = build_menu(sess, lang)
        o = resolve_option(m, a.option)
        rev = json.loads(a.revision) if a.revision else _parse_set(a.sets)
        if not rev:
            rev = None
        d = build_decision(o, revision=rev, note=a.note, stage_id=m["await"]["stage_id"])
        err = dry_run_validate(sess, d)
        if err:
            _print({"ok": False, "error": err, "option": o["n"], "decision": d}, a.as_json)
            return 2
        if not a.apply:
            _print({"ok": True, "dry_run": True, "option": o["n"],
                    "decision": d, "would_resume": path}, a.as_json)
            return 0
        res = apply_decision(path, d, debug=a.debug)
        _print({"ok": True, "applied": True,
                "await": (res.get("fullflow") or {}).get("await"),
                # 批准后自动产出的交付物（如 A2 检索结果 xlsx），供 agent 直接呈现
                "artifacts": res.get("artifacts") or [],
                "error": res.get("error")}, a.as_json)
        return 0
    except MenuError as e:
        _print({"ok": False, "error": str(e)}, a.as_json)
        return 2
    except FileNotFoundError as e:
        _print({"ok": False, "error": f"会话不可读：{e}"}, a.as_json)
        return 3


if __name__ == "__main__":
    sys.exit(main())
