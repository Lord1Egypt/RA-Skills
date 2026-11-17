# -*- coding: utf-8 -*-
"""Phase 1 · Block A 本地优先管线驱动器（方向确定与文献/数据准备）。

设计约束（对齐 contracts/pipeline_stage/v1.0.0/SPEC.md §9 / roadmap Phase 1）：

- **不依赖 coze 部署**：本模块完全本地运行，不调用 run_stage/run_meta，因此不会触发
  出站鉴权（AuthRequiredError）。A2 检索委派走本地 ct-literature（tool_card →
  execute_tool_cards 本地 subprocess），A4 红线闸本地强执。
- A1/初筛的「AI 生成大脑」在 coze 侧（尚未部署），此处提供**本地启发式兜底 + 合规信封**，
  coze 部署后可由 run_stage 无缝接管（seam 见 run_block_a 的 `use_coze` 占位）。
- 阶段序列（SPEC §9；用户裁定 2026-09-10 起 A2/A3 合并）：
    A1.topic_selection    选题闸门
    A2.literature_search  文献集 = 检索委派 ct-literature（tool_card）+ 同节点内去重/规则初筛
    A4.data_extraction    提取 AI 草稿 + 🔴 extraction_review 人工核验闸
- 返回结构与 run_pipeline 同构：{done, await_human, gate, final, stages[], attachments[],
  tool_card_outputs[]}，便于上层统一消费。

依赖：coze_client（提供 CONTRACT_VERSION / STAGE_SCHEMA_ID / execute_tool_cards /
_REDLINE_GATES）。所有网络动作在 execute_tool_cards 内部，测试可 monkeypatch。
"""

import hashlib
import json
import os
import re
import shutil
import sys
import uuid

import coze_client as cc
import features  # 网页功能开关（2026-09-17：A4 数据提取可隐藏，仅保留下载）

# 2026-09-24：本地选题评估增强（registry 探针 + 确定性评分器）
import registry_probe as _registry_probe
import topic_assess
import prospero_probe as _prospero_probe

# A2 检索式翻译关联 ct-base 权威 kw_localize（ct-base 规范 bilingual_retrieval.md）：
# 本模块不重复实现翻译，仅在首次需要时把「ct-base/scripts → ct-literature/scripts
# → 载荷 bundled/ct-literature/scripts」中首个可用者加入 sys.path 后复用。
# ⚠️ 2026-09-17 修复：原实现硬编码本机技能树路径，**发布沙箱里该路径不存在**，
#   import 必然失败 → 翻译静默降级（中文检索式原样送国际库），且 fully_translated
#   仍报 True（谎报）。现由 _kw_localize_scripts_dir() 逐级回落，见其实现。
_CT_BASE_SCRIPTS = os.path.expanduser("~/.workbuddy/skills/ct-base/scripts")

# ---- Block A 阶段 ID（SPEC §9，严格匹配 coze 端编排对齐） ----
# 用户裁定（2026-09-10）：A2 检索 与 A3 初筛 **合并为单节点 A2**（「文献集」）。
# 检索完成后**同节点内**立刻跑去重 + 规则初筛，只软停一次、只产出**一张**合并表
# （检索结果 + 裁决/理由/文献类型确认列）。A3 不再作为独立阶段出现在块序列里，
# 但常量保留：screening 相关函数与旧会话（含 A3 阶段）的兼容回读都要用它。
A1 = "A1.topic_selection"
A2 = "A2.literature_search"
# 用户裁定（2026-09-17）：A3 恢复为**独立节点 = PDF 全文下载**（从 A4 拆出）；
# A4（数据提取）保留但默认隐藏备用（见 features.a4_extraction）。
# ⚠️ A3 有两代含义，务必区分：
#   A3_LEGACY = "A3.screening"     —— 旧「初筛」阶段（2026-09-10 已并入 A2）；
#                                     仅用于**旧会话兼容回读**，不得用于新编排。
#   A3        = "A3.pdf_download"  —— 新「PDF 全文下载」独立阶段。
A3_LEGACY = "A3.screening"  # 旧会话兼容专用（并入 A2 前的历史快照仍停在它上面）
A3 = "A3.pdf_download"      # PDF 全文下载（2026-09-17 从 A4 拆出的独立节点）
A4 = "A4.data_extraction"   # 数据提取（隐藏备用，features.a4_extraction 开启时启用）
BLOCK_A_SEQUENCE = [A1, A2, A3, A4]
BLOCK_A_TOTAL = len(BLOCK_A_SEQUENCE)


# ---------------------------------------------------------------------------
# 信封构造（本地「prompt → 合法入参」层；与 SPEC §2/§3 一致）
# ---------------------------------------------------------------------------
def build_block_a_env(topic, max_results=50, year_from=None,
                      pipeline_id=None, query_origin=None):
    """构造 Block A 初始 stage 信封（请求侧）。

    补齐 contract_version / schema / pipeline(block='A') / stage(A1) / stage_context。
    仅结构化必填校验，无领域判断。topic 经 params.topic 透传，下游 A2 复用。
    """
    env = {
        "contract_version": cc.CONTRACT_VERSION,
        "schema": cc.STAGE_SCHEMA_ID,
        "pipeline_id": pipeline_id or f"blkA-{uuid.uuid4().hex[:8]}",
        "pipeline": {"name": "block_a", "block": "A", "cfg": {}},
        "request_id": str(uuid.uuid4()),
        "task": "topic_selection",
        "params": {"topic": topic, "max": max_results},
        "stage": {
            "id": A1, "index": 0, "total": BLOCK_A_TOTAL,
            "intent": "run", "prev_stage_id": None,
        },
        "stage_context": {"human_decisions": [], "tool_card_outputs": [], "artifacts": []},
    }
    if year_from is not None:
        env["params"]["year_from"] = year_from
    if query_origin:
        env["query_origin"] = query_origin
    return env


# ---------------------------------------------------------------------------
# 阶段响应构造（与 parse_stage_response 输出同构，便于统一消费）
# ---------------------------------------------------------------------------
def _mk_stage(sid, index, status, stage_result, nha, tool_cards=None):
    nha = nha or {}
    return {
        "mode": "stage",
        "stage": {"id": sid, "index": index, "total": BLOCK_A_TOTAL, "status": status,
                  "prev_stage_id": BLOCK_A_SEQUENCE[index - 1] if index > 0 else None},
        "stage_result": stage_result,
        "next_human_action": nha,
        "tool_cards": tool_cards or [],
        "_gate_blocked": bool(
            nha.get("gate") in cc._REDLINE_GATES and nha.get("required")
        ),
    }


# ---------------------------------------------------------------------------
# A1 选题闸门（本地启发式兜底；coze 部署后由其接管双库评分 + PROSPERO 查重）
# ---------------------------------------------------------------------------
def _infer_picos(topic):
    """极简 PICOS 启发式：按常见分隔符/关键词切分，标注缺失维度。
    仅离线兜底用，精度有限，结果须人工确认。"""
    t = (topic or "").strip()
    parts = [p.strip() for p in t.replace("；", ";").replace("；", ";").split(";") if p.strip()]
    picos = {"P": None, "I": None, "C": None, "O": None, "S": None}
    for i, p in enumerate(parts[:4]):
        picos[list(picos.keys())[i]] = p
    # 关键词兜底：含「vs/对照/安慰剂」→ 推断 C
    if picos["C"] is None and any(k in t.lower() for k in ("vs", "对照", "placebo", "安慰剂")):
        picos["C"] = "（疑似含对照，待确认）"
    missing = [k for k, v in picos.items() if v is None]
    return picos, missing


def _try_coze_topic_assessment(topic, picos, missing, assess_draft, registry_probe, dedup_probe, prospero):
    """P1 结构：调用 coze topic_assessment 节点取临床价值判断 + 选题策展。

    默认关闭（META_TOPIC_COZE 未置 1）。待 coze 侧 topic_assessment 节点就绪（P2/P3）
    后将环境变量置 1 启用。复用 ct-meta 端点（已在 auto_approve_endpoints 白名单），
    不新增鉴权。任何异常/未授权/节点缺/返回缺字段 -> 返回 None，本地默认中值降级，
    绝不阻断选题流程。
    """
    if not os.environ.get("META_TOPIC_COZE"):
        return None
    try:
        cochrane_hits, pubmed_hits = topic_assess._extract_dedup_counts(dedup_probe)
        data = {
            "topic": topic,
            "picos": picos,
            "missing_picos": missing,
            "evidence": {
                "dedup": {"cochrane_hits": cochrane_hits, "pubmed_sr_ma_hits": pubmed_hits},
                "registry": {"status": (registry_probe or {}).get("status"),
                             "total": (registry_probe or {}).get("total")},
                "prospero": {"status": (prospero or {}).get("status"),
                             "error": (prospero or {}).get("error")},
            },
            "deterministic_scores": {
                "method": assess_draft.get("scores", {}).get("feasibility"),
                "data": assess_draft.get("scores", {}).get("data"),
                "novelty": assess_draft.get("scores", {}).get("novelty"),
            },
            "rules": {
                "cross_checks": assess_draft.get("cross_checks"),
                "compliance": assess_draft.get("compliance"),
            },
        }
        res = cc.run_meta("topic_assessment", data=data,
                          params={"user_language": "zh"}, timeout=45)
        if not isinstance(res, dict) or res.get("status") != "ok":
            return None
        clin = res.get("clinical") or {}
        if "score" not in clin:
            return None
        out = {"clinical": {"score": clin.get("score"), "rationale": clin.get("rationale")}}
        if isinstance(res.get("curation"), dict):
            out["curation"] = res["curation"]
        return out
    except Exception:  # noqa: BLE001 -- coze 不可达/未授权/节点缺 -> 降级
        return None


def _llm_clinical_fallback(topic, picos, missing, draft):
    """临床价值维度的后台大模型评估（ct-base §12；2026-09-25 用户指令）。

    背景：coze 路径（META_TOPIC_COZE）默认关，发布版 sandbox 里没有 Agent/coze 在
    回路 → 此前临床价值只能取「默认中值 + 需人工」提示。现改为走 topic_translate
    同款端点梯队（本地 models.json 快源优先；云端唯一候选 = LongCat-2.0 混淆 key），
    产 {score, rationale} 作 clinical_override。任何失败返回 None，维持原中值降级。

    磁盘缓存按 topic+picos 指纹：速览按钮重复点不重复花额度。
    """
    import time as _time
    try:
        import topic_translate as _tt
        cands = _tt._candidates()
        if not cands:
            return None
        key = hashlib.sha1(("%s|%s" % (topic, json.dumps(
            picos, sort_keys=True, ensure_ascii=False))).encode("utf-8")).hexdigest()
        cache_p = os.path.join(_tt._local_dir(), "clinical_cache.json")
        try:
            with open(cache_p, "r", encoding="utf-8") as f:
                cache = json.load(f)
            if not isinstance(cache, dict):
                cache = {}
        except Exception:
            cache = {}
        hit = cache.get(key)
        if isinstance(hit, dict) and isinstance(hit.get("score"), int):
            return {"score": hit["score"], "rationale": hit.get("rationale") or None}
        sc = draft.get("scores") or {}
        sys_prompt = (
            "你是临床试验方法学与临床价值评估专家。对给定的系统综述/Meta 分析选题，"
            "评估其**临床价值**维度（0-5 分：是否回应真实临床决策需求——药物、剂量、"
            "人群、结局是否影响实践；是否已被充分回答）。"
            "综合提供的选题、PICOS 与确定性评分佐证信息。"
            '只输出一个 JSON 对象：{"score": <0-5 整数>, "rationale": "<一句话中文依据，不超过80字>"}'
            "，不要解释、不要代码围栏。")
        user = json.dumps({
            "topic": topic, "picos": picos, "missing_picos": missing,
            "deterministic_scores": {"method": sc.get("feasibility"),
                                      "data": sc.get("data"),
                                      "novelty": sc.get("novelty")},
        }, ensure_ascii=False)
        for base, k, model in cands:
            try:
                raw = _tt._call(base, k, model, user, timeout=35,
                                system=sys_prompt, raw=True)
            except Exception:  # noqa: BLE001 - 逐候选降级
                continue
            got = _tt._loads_json_obj(raw)
            try:
                score = int(got.get("score"))
            except (TypeError, ValueError):
                continue
            if not 0 <= score <= 5:
                continue
            rationale = str(got.get("rationale") or "").strip()[:200] or None
            cache[key] = {"score": score, "rationale": rationale,
                          "model": model, "ts": int(_time.time())}
            try:
                os.makedirs(os.path.dirname(cache_p), exist_ok=True)
                with open(cache_p, "w", encoding="utf-8") as f:
                    json.dump(cache, f, ensure_ascii=False)
            except Exception:
                pass  # 缓存写失败不阻断
            return {"score": score, "rationale": rationale}
        return None
    except Exception:  # noqa: BLE001 - 兜底评估失败维持中值
        return None


def a1_topic_selection(topic, registry_probe=None, dedup_probe=None, run_local_assessment=True, topic_en=None):
    picos, missing = _infer_picos(topic)
    # 范围预警：过短/过长或缺失维度过多 → 提示收窄
    scope_warning = None
    if len(topic or "") < 6:
        scope_warning = "选题过短，可能检索噪声过大，建议补充 P/I/C/O 维度。"
    elif missing and len(missing) >= 3:
        scope_warning = f"PICOS 缺失维度过多（{', '.join(missing)}），建议先明确研究问题。"
    report = {
        "topic": topic,
        "picos": picos,
        "missing_dimensions": missing,
        "scope_warning": scope_warning,
        "coze_ready": False,
        "note": "本地启发式兜底；双库（Cochrane/PubMed）探针评分与 PROSPERO 查重需 coze 或 ct-registry 支持。",
        # 新增：选题可行性评估（拥挤度 / 证据量 / 方向稀缺度）
        "feasibility": {"crowding": "unknown", "expected_studies": None, "risk_alert": None},
    }
    # 2026-09-24：registry_probe 为 None 时本地直连 ClinicalTrials.gov 取真实注册数
    if registry_probe is None:
        try:
            registry_probe = _registry_probe.probe_local(topic)
        except Exception as _e:  # noqa: BLE001
            registry_probe = {"status": "error", "total": None, "returned": None,
                              "sample": [], "note": f"本地 registry 探针失败: {_e}"}
    # 2026-09-24：PROSPERO 自动检索探针（真实尝试 + 优雅降级，上游故障时标 unavailable）
    # 2026-09-25：优先用英文检索词（PROSPERO 是英文注册库，中文 topic 检索≈0 命中）
    try:
        _prospero = _prospero_probe.probe(topic_en or topic)
    except Exception as _pe:  # noqa: BLE001
        _prospero = {"status": "unavailable", "hit_count": None, "sample": [],
                     "error": f"PROSPERO 探针失败: {_pe}", "manual_url": None, "note": ""}
    # A1 查重探针：真实调 ct-registry（CT.gov 来源）已注册试验数，供选题拥挤度判断
    if registry_probe:
        report["registry_probe"] = registry_probe
        total = registry_probe.get("total")
        if total is not None:
            if total == 0:
                report["scope_warning"] = (report["scope_warning"] or "") + " 注册库未检索到相关试验，属空白/新兴方向。"
                report["feasibility"]["crowding"] = "empty"
                report["feasibility"]["risk_alert"] = "⚠️ 方向空白，可能原始研究极少，预期可纳入研究数量不足（meta 至少 k≥2）。"
            elif total < 5:
                report["feasibility"]["crowding"] = "low"
                report["feasibility"]["expected_studies"] = total
                report["feasibility"]["risk_alert"] = f"⚠️ 注册库仅 {total} 项，预期可纳入研究较少，meta 分析效能可能不足。"
            elif total >= 200:
                report["scope_warning"] = (report["scope_warning"] or "") + f" 注册库已检索到 {total} 项相关试验，方向可能已较拥挤，建议明确差异化角度。"
                report["feasibility"]["crowding"] = "high"
                report["feasibility"]["expected_studies"] = total
            else:
                report["feasibility"]["crowding"] = "moderate"
                report["feasibility"]["expected_studies"] = total

    # 2026-09-24：本地确定性选题评分（4 维 + R1-R6 + PRISMA/AMSTAR-2 预检 + real-gap）
    if run_local_assessment:
        try:
            _assess = topic_assess.assess(
                topic=topic, picos=picos, missing=missing,
                dedup=dedup_probe, registry=registry_probe, prospero=_prospero,
                topic_en=topic_en,
            )
            # 2026-09-24：coze 临床价值判断 + 选题策展（P1 结构就位，默认关；
            # META_TOPIC_COZE=1 且 coze 节点就绪后启用；失败自动降级默认中值）
            _coze = _try_coze_topic_assessment(
                topic, picos, missing, _assess, registry_probe, dedup_probe, _prospero)
            # 2026-09-25：coze 不可用时，走后台大模型（LongCat-2.0 等）评估临床价值，
            # 不再静默取默认中值。任何失败仍回退中值（_llm_clinical_fallback 返回 None）。
            _clinical = None
            _curation = None
            if _coze:
                _clinical = _coze.get("clinical")
                _curation = _coze.get("curation")
            if not _clinical:
                _clinical = _llm_clinical_fallback(topic, picos, missing, _assess)
            if _clinical:
                _assess = topic_assess.assess(
                    topic=topic, picos=picos, missing=missing,
                    dedup=dedup_probe, registry=registry_probe, prospero=_prospero,
                    clinical_override=_clinical, curation=_curation,
                )
            report["topic_analysis"] = _assess
        except Exception as _ae:  # noqa: BLE001
            report["topic_analysis"] = {"error": f"本地评分失败: {_ae}"}

    # 供工作台 A1 面板「PICOS 报告」文本框预填（editable_payload.report 的源）
    # —— 对齐 EDITABLE_KEYS["A1.topic_selection"]=["report"]，避免文本框空白。
    # 2026-09-19（用户需求）：该报告经 _picos_report_to_query 变成 A2 检索主题，
    # 预填**只保留 PICOS 五维表格**（缺失=（待填），解析时自动跳过），保证
    # 「原始主题（输入）」干净。缺失维度/拥挤度/注册库探针/后续步骤等系统信号
    # 改由 A1 只读面板（系统检查 / 可行性信号）展示，不再混进可编辑文本。
    _rep = ["| 维度 | 内容 |", "| --- | --- |"]
    # 五维全空 → P 行放原始主题（用户仍能看到自己的选题，其余行待填）；否则按推断值。
    _p_val = picos.get("P") or (topic if not any(picos.values()) else "（待填）")
    _rep.append(f"| P | {_p_val} |")
    for _k in ("I", "C", "O", "S"):
        _rep.append(f"| {_k} | {picos.get(_k) or '（待填）'} |")
    report["report"] = "\n".join(_rep)
    nha = {
        "type": "confirm",
        "prompt": f"选题闸门（本地启发式）{'+ ct-registry 查重' if registry_probe else ''}：{topic}。"
                  f"{scope_warning or '维度基本完整，请确认方向。'}",
        "required": True,
        "gate": "none",
    }
    return report, nha


# ---------------------------------------------------------------------------
# A1 查重探针：真实调 ct-registry（选题闸门补充，非阻塞）
# ---------------------------------------------------------------------------
def _read_registry_xlsx(xlsx_path, limit=5):
    """从 ct-registry 落盘的 report.xlsx「试验总表」抽取样本（登记号/标题/状态/国家/注册日期）。

    ct-registry 跑完会清理中间 json、仅保留 ./out/report.xlsx，故读 xlsx。表头为中文，按子串匹配列。
    """
    import openpyxl
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    target = "试验总表" if "试验总表" in wb.sheetnames else (wb.sheetnames[1] if len(wb.sheetnames) > 1 else None)
    if not target:
        return []
    ws = wb[target]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    header = [str(c or "").strip() for c in rows[0]]
    col = {}
    for i, h in enumerate(header):
        for key, name in (("id", "登记号"), ("title", "标题"), ("status", "状态"),
                          ("country", "国家"), ("date", "注册日期")):
            if name in h and key not in col:
                col[key] = i
    sample = []
    for r in rows[1:]:
        if not any(r):
            continue
        rec = {k: (str(r[i]).strip() if i < len(r) and r[i] is not None else None) for k, i in col.items()}
        if rec.get("title") or rec.get("id"):
            sample.append(rec)
        if len(sample) >= limit:
            break
    return sample


def a1_registry_check(topic, max_results=10, workdir=None):
    """真实调 ct-registry 做选题查重探针。

    ct-registry 特性（须适配）：① 必须带 --run 才发网络（fixed_flags 已加）；② 忽略 --out-dir、
    把结果写相对 ./out 且仅保留 report.xlsx（中间 json 被清理）。故在临时 cwd 跑，再从
    <workdir>/out/report.xlsx 读样本；同时解析 stdout 日志的 `[ctgov] total=N returned=M` 取总数。
    返回 {status, total, returned, sample[], note}。失败/缺依赖优雅降级，不阻断 A1。
    """
    import os
    import re
    import tempfile
    if workdir is None:
        workdir = tempfile.mkdtemp(prefix="a1reg_")
    card = {
        "card_ref": "A1-ct-registry",
        "need_tool": "ct-registry",
        "params": {"condition": topic, "max": max_results},
        "sync": "blocking",
        "timeout_sec": 180,
    }
    outs = cc.execute_tool_cards([card], out_dir=workdir, cwd=workdir)
    probe = {"status": "error", "total": None, "returned": None, "sample": [], "note": ""}
    if not outs:
        probe["note"] = "ct-registry 无返回（映射缺失？）"
        return probe
    o = outs[0]
    probe["status"] = o.get("status")
    log = o.get("result") or ""
    if isinstance(log, str):
        m = re.search(r"\[ctgov\]\s*total=(\d+)\s*returned=(\d+)", log)
        if m:
            probe["total"] = int(m.group(1))
            probe["returned"] = int(m.group(2))
    xlsx = os.path.join(workdir, "out", "report.xlsx")
    if os.path.isfile(xlsx):
        try:
            probe["sample"] = _read_registry_xlsx(xlsx)
        except Exception as e:  # noqa: BLE001
            probe["note"] = f"xlsx 解析失败: {type(e).__name__}: {e}"
    else:
        probe["note"] = (probe["note"] or "") + " report.xlsx 未生成（可能检索无结果或 skill 异常）。"
    return probe


# ---------------------------------------------------------------------------
# A2 检索委派 ct-literature（真实本地执行，不经 coze）
# ---------------------------------------------------------------------------
def a2_build_tool_card(topic, max_results=50, year_from=None, out_dir=".",
                       include_reviews=False, sources=None):
    """Build the ct-literature tool card for A2 retrieval.

    include_reviews (default False): when False, review-type publications are
    excluded at the source (Europe PMC + OpenAlex both filter them out), so the
    retrieval quota is spent on original studies rather than reviews that would
    be excluded by A3 review-guard anyway. Set True for umbrella-review or
    scoping-review scenarios where reviews are the target evidence.
    sources (default None): 检索数据源子集，如 ["OpenAlex","EuropePMC"]（规范名见
    AVAILABLE_SOURCES）。None = ct-literature 默认全量；非空则序列化为逗号串写入
    params.sources，经 tool_mapping 的 "sources": "--sources" 透传给 ct-literature。"""
    params = {"topic": topic, "max": max_results, "out_dir": out_dir,
              "include_reviews": include_reviews}
    if year_from is not None:
        params["year_from"] = year_from
    if sources:
        # execute_tool_cards 对 arg_map 值做 str(val)；列表会被序列化成 "['A', 'B']"，
        # ct-literature 的 --sources 无法解析。故此处归一为逗号分隔串。
        params["sources"] = (sources if isinstance(sources, str)
                             else ",".join(str(s) for s in sources))
    return {
        "card_ref": "A2-ct-literature",
        "need_tool": "ct-literature",
        "params": params,
        "sync": "blocking",
        "timeout_sec": 120,
    }


def _extract_studies(res):
    """从 ct-literature 输出中尽力抽取文献列表（兼容多种返回形态）。"""
    if isinstance(res, list):
        return res
    if isinstance(res, dict):
        for k in ("studies", "papers", "results", "records", "items", "data"):
            v = res.get(k)
            if isinstance(v, list):
                return v
        # 嵌套 data 再探一层
        d = res.get("data")
        if isinstance(d, dict):
            for k in ("studies", "papers", "results", "records", "items"):
                if isinstance(d.get(k), list):
                    return d[k]
    return []


def _normalize_works(works):
    """把 ct-literature 本地 --out-dir 文件 或 云端 ct-search search_literature()
    返回的 works[] 统一归一化为 studies[]（字段对齐 A2/A3 下游消费）。
    journal 兼容三种来源：本地 publication / 本地 journal / 云端 journal_iso；
    abstract 回退到 abstract_snippet。按 doi/title 去重。
    """
    studies = []
    seen = set()
    for w in works:
        if not isinstance(w, dict):
            continue
        key = str(w.get("doi") or w.get("title") or "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        studies.append({
            "title": w.get("title"),
            "year": w.get("year") or w.get("publication_year"),
            "doi": w.get("doi"),
            "source": w.get("source"),
            "pmid": w.get("pmid"),
            "is_retracted": bool(w.get("is_retracted")),
            "url": w.get("url") or w.get("open_access_url"),
            # 检索阶段已抓回的摘要片段，透传到 A3 筛选 / 下载前相关性判断
            "abstract_snippet": w.get("abstract_snippet") or w.get("abstract"),
            # ---- 人工裁决所需元数据（A3 逐条决策要凭刊名/作者/设计等判断相关性）----
            # 这些字段 ct-literature 的 work 里本来就有，此前归一化时被丢弃，
            # 导致 A3 界面只能看到标题。此处按需捞回，缺值一律 None（不臆造）。
            "journal": w.get("journal") or w.get("publication") or w.get("journal_iso"),
            "authors": w.get("authors") if isinstance(w.get("authors"), list) else None,
            "publication_date": w.get("publication_date"),
            "volume": w.get("volume"),
            "issue": w.get("issue"),
            "page": w.get("page"),
            "study_type": w.get("study_type"),
            "type": w.get("type"),
            "cited_by_count": w.get("cited_by_count"),
            "keywords": w.get("keywords") if isinstance(w.get("keywords"), list) else None,
            "relevance_score": w.get("relevance_score"),
            "language": w.get("language"),
            "is_safety": bool(w.get("is_safety")),
        })
    return studies


# 云端 ct-search（search_literature）支持的 source 列表（与 ct_literature 共用 Coze 端点）
_CLOUD_SOURCE_ALIASES = {
    "openalex": "openalex", "OpenAlex": "openalex",
    "europepmc": "europepmc", "EuropePMC": "europepmc", "europe pmc": "europepmc",
    "pubmed": "europepmc", "PubMed": "europepmc",  # europepmc 覆盖 PubMed 内容
    "biorxiv": "biorxiv", "medrxiv": "medrxiv",
    "semantic_scholar": "semantic_scholar", "arxiv": "arxiv",
}


def _map_sources_to_cloud(sources):
    """把 A2 的 sources 子集（如 ["OpenAlex","EuropePMC"]）映射为云端支持的 source 列表。
    None/空 → 默认 [europepmc, openalex]（合并两源更全）；PubMed 归并到 europepmc。
    """
    if not sources:
        return ["europepmc", "openalex"]
    out = []
    for s in (sources if isinstance(sources, list) else [sources]):
        key = _CLOUD_SOURCE_ALIASES.get(s if isinstance(s, str) else str(s))
        if key and key not in out:
            out.append(key)
    return out or ["europepmc"]


def _cloud_literature_search(topic, max_results=50, year_from=None, sources=None):
    """云端 ct-search 回退检索（与 a2_build_tool_card 本地 subprocess 路径互斥）。

    当本地 ct-literature 技能不可用（沙箱/未安装场景）时启用：
    直接调用 ctsearch_client.search_literature()——纯 urllib，走公开 token，
    无需在沙箱里安装 ct-literature 技能。返回归一化 studies[]。
    """
    try:
        from ctsearch_client import search_literature
    except Exception:
        return []
    collected = []
    seen_keys = set()
    for src in _map_sources_to_cloud(sources):
        try:
            res = search_literature(
                keyword=topic, source=src, max_results=max_results,
                year_from=year_from, timeout=300)
        except Exception:
            continue
        if res.get("error") or not res.get("works"):
            continue
        for s in _normalize_works(res["works"]):
            k = str(s.get("doi") or s.get("title") or "").strip().lower()
            if k and k not in seen_keys:
                seen_keys.add(k)
                collected.append(s)
    return collected


def _read_literature_dir(out_dir):
    """真实 ct-literature 把数据写入 --out-dir 文件（.merged.json 的 works[]，
    或各源 openalex.json/europepmc.json 的 works[]），stdout 仅日志。
    此处回退读取并归一化为 studies[]，去重。
    """
    import glob
    import os
    out_dir = os.path.abspath(out_dir)
    if not os.path.isdir(out_dir):
        return []
    merged = os.path.join(out_dir, ".merged.json")
    files = [merged] if os.path.isfile(merged) else sorted(glob.glob(os.path.join(out_dir, "*.json")))
    works = []
    for p in files:
        try:
            data = json.load(open(p, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        w = data.get("works") if isinstance(data, dict) else (data if isinstance(data, list) else [])
        if isinstance(w, list):
            works.extend(w)
    return _normalize_works(works)


def a2_search_fingerprint(translated_query, max_results, year_from,
                          include_reviews, sources):
    """A2 检索指纹（2026-09-20）：本次检索输入的确定性摘要，用于回退时判断能否复用上次结果。

    覆盖**全部会改变检索结果的输入**：优化翻译后的检索式、结果上限、年限、是否纳入综述、
    数据源子集。任一改动 → 指纹变化 → 自动回到真实联网检索，不会静默给旧结果。
    不含 topic/原始检索式：翻译前后同义的输入应视为同一检索（翻译结果已进指纹）。

    用途：打回/回退到 A 块时，`rewind()` 保留上一轮信封作为复用源；`run_block_a` 用它
    比对指纹，一致就跳过 A1 查重探针（≤180s 超时）与 A2 全库检索（代码注释实测约 2 分钟），
    只重跑规则初筛并在 A2 闸重新停下等人工确认。
    """
    payload = json.dumps({
        "q": str(translated_query or "").strip(),
        "max_results": max_results,
        "year_from": year_from,
        "include_reviews": bool(include_reviews),
        "sources": sorted(str(s) for s in (sources or [])),
    }, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def a2_literature_search(topic, max_results=50, year_from=None, out_dir=".",
                         on_line=None, include_reviews=False, sources=None):
    """构建 ct-literature tool_card → execute_tool_cards 本地执行 → 解析文献列表。

    include_reviews：是否允许综述类文献进入检索结果。默认 False（源头排除），
    节省检索配额；仅在伞评/范围综述等需要综述作为证据时设为 True。
    sources：要检索的数据库子集（如 ["OpenAlex","EuropePMC","PubMed"]）。None = 用
    ct-literature 默认全量；非空则作为 scope 写入 tool_card params，供 ct-literature
    按选定库检索（其支持时生效；不支持时该字段作为声明性 scope 保留，便于审计）。
    """
    card = a2_build_tool_card(topic, max_results, year_from, out_dir=out_dir,
                              include_reviews=include_reviews, sources=sources)
    outs = cc.execute_tool_cards([card], out_dir=out_dir, on_line=on_line)
    studies = []
    if outs:
        o = outs[0]
        if o.get("status") == "ok":
            studies = _extract_studies(o.get("result") or {})
        if not studies:  # 真实 ct-literature：读 --out-dir 文件
            studies = _read_literature_dir(out_dir)
    # 云端 ct-search 回退：本地 ct-literature 技能不可用（沙箱/未安装）时，
    # 直接走 ctsearch_client.search_literature() 云端检索，无需嵌入兄弟技能。
    if not studies:
        studies = _cloud_literature_search(topic, max_results, year_from, sources)
    return studies, outs, card


# ---------------------------------------------------------------------------
# A3 筛选（本地启发式：去重 + 简单纳入标记；coze 部署后由其接管 AI 筛选）
# ---------------------------------------------------------------------------
def _heuristic_include(study, inclusion_hints=None):
    """极简纳入启发式（离线兜底）：排除关键词命中则剔除；若提供纳入关键词，
    则要求标题或摘要片段命中至少一项才纳入，否则标为待人工核验。
    摘要 abstract_snippet 现已透传进 study，故此判断已具备摘要级依据。"""
    text = " ".join(str(v) for v in (study or {}).values() if isinstance(v, (str, int)))
    text = text.lower()
    exclude = ["retracted", "撤稿", "abstract only", "protocol", "letter"]
    if any(k in text for k in exclude):
        return False, "命中排除关键词（离线启发式）"
    hints = [str(h).lower() for h in (inclusion_hints or []) if h]
    if hints:
        if any(h in text for h in hints):
            return True, "标题/摘要命中纳入关键词（离线启发式）"
        return False, "未命中纳入关键词，待人工核验相关性"
    return True, "默认纳入（离线启发式，待人工确认）"


# ---------------------------------------------------------------------------
# A3 review-guard：综述/二次研究检测（零幻觉、纯关键词；*警告*信号，不覆盖人工裁决）
# 目的：综述/meta 本身无原始 2×2 表，送进 A4 抽取只会 0 行、浪费配额。在 A3 打标 +
# A4 抽取前软警告，让人先判断是否排除，而非静默抽空。
# ---------------------------------------------------------------------------
_REVIEW_STRONG = re.compile(
    r"systematic review|meta[- ]?analysis|scoping review|umbrella review|"
    r"overview of (the )?(literature|studies|reviews)|rapid review|narrative review|"
    r"literature review|pooled analysis|quantitative synthesis|"
    r"系统综述|荟萃分析|meta\s*分析|范围综述|伞状综述|综述", re.I)
# 规律 R1 回流（2026-09-09 15 篇实证：9/15 为指南/共识/声明，同样无原始 2×2）：
# 指南/共识/声明与综述同级默认排除（人工裁决优先，不覆盖翻纳入）
_GUIDELINE_STRONG = re.compile(
    r"clinical practice guideline|practice guideline|guidelines? (for|on|the)\b|"
    r"consensus (statement|conference|report|on)|position statement|"
    r"presidential advisory|expert (consensus|panel|recommendations?)|"
    r"recommendations? (for|of|on) (the )?(management|diagnosis|treatment|prevention)|"
    r"临床指南|专家共识|诊疗指南|指南|共识声明", re.I)
_REVIEW_WEAK = re.compile(r"\b(review|综述)\b", re.I)
_REVIEW_WEAK_EXCLUDE = re.compile(r"(peer|under|in)\s+review\b", re.I)


def is_likely_review(study):
    """标题/摘要级综述·指南检测。返回 (bool, reason_or_None)。

    - ★B1 (2026-09-04) 优先采信 API 权威 pubType 字段：study["pub_types"]
      （Europe PMC pubTypeList / OpenAlex / Crossref type 经 literature_probe 归一化入），
      含 "review" 变体即 100% 判综述——这是出版商自标 "Review" 标签的元数据等价物，
      比关键词可靠；API 未标注的综述仍由下方关键词兜底（不误判、不漏判）。
    - 强短语（systematic review / meta-analysis / 系统综述 / 荟萃分析 …）直接判综述；
    - 规律 R1：指南/共识/声明强短语同判（guideline / consensus / position statement /
      专家共识…）——同样无原始 2×2 数据，实证占抽取失败的 9/15；
    - 弱信号（裸 review/综述）接受，但排除「peer/under/in review」误伤；
    - 纯*警告*：绝不把 include 翻成 exclude，人工裁决优先。
    """
    if not isinstance(study, dict):
        return False, None
    # ★B1：pubType 硬信号优先（有则采信，零误判）
    _pts = study.get("pub_types")
    if isinstance(_pts, list):
        for _pt in _pts:
            if isinstance(_pt, str) and re.search(r"review", _pt, re.I):
                return True, f"pubType 标注综述：{_pt.strip()}"
            if isinstance(_pt, str) and re.search(r"guideline|consensus|practice guideline",
                                                  _pt, re.I):
                return True, f"pubType 标注指南/共识：{_pt.strip()}"
    title = str(study.get("title") or "")
    abstract = str(study.get("abstract_snippet") or study.get("abstract") or "")
    text = (title + " " + abstract).lower()
    m = _REVIEW_STRONG.search(text)
    if m:
        return True, f"命中综述特征：{m.group(0).strip()}"
    m = _GUIDELINE_STRONG.search(text)
    if m:
        return True, f"命中指南/共识特征：{m.group(0).strip()}（无原始 2×2）"
    if _REVIEW_WEAK.search(text) and not _REVIEW_WEAK_EXCLUDE.search(text):
        return True, "标题/摘要含 review/综述（弱信号）"
    return False, None


# ---------------------------------------------------------------------------
# 文献类型：规则预填 → 人工在 A3 裁决表确认 → A4 只读（不再判定）
# ---------------------------------------------------------------------------
# 单一词表，三处同源（meta 此处 / ct-literature doc_type_filter.classify_record /
# meta pdf_extractor.classify_pdf），不自造第二套：
#   original | review | guideline | protocol | unknown
DOC_TYPE_ORIGINAL = "original"
DOC_TYPE_REVIEW = "review"
DOC_TYPE_GUIDELINE = "guideline"
DOC_TYPE_PROTOCOL = "protocol"
DOC_TYPE_UNKNOWN = "unknown"
DOC_TYPE_ORDER = (DOC_TYPE_ORIGINAL, DOC_TYPE_REVIEW, DOC_TYPE_GUIDELINE,
                  DOC_TYPE_PROTOCOL, DOC_TYPE_UNKNOWN)
# 无原始 2×2 数据的类型：仅用于提示文案与徽标，**不再构成任何排除判定**
DOC_TYPE_NO_PRIMARY = (DOC_TYPE_REVIEW, DOC_TYPE_GUIDELINE, DOC_TYPE_PROTOCOL)
# 导出表下拉显示标签（人工可读；回传经 _norm_doc_type 归一为 internal 值）
DOC_TYPE_LABELS = {
    DOC_TYPE_ORIGINAL: "原创研究",
    DOC_TYPE_REVIEW: "综述/Meta",
    DOC_TYPE_GUIDELINE: "指南/共识",
    DOC_TYPE_PROTOCOL: "研究方案",
    DOC_TYPE_UNKNOWN: "不确定",
}
DOC_TYPE_LABELS_EN = {
    DOC_TYPE_ORIGINAL: "Original research",
    DOC_TYPE_REVIEW: "Review/Meta",
    DOC_TYPE_GUIDELINE: "Guideline",
    DOC_TYPE_PROTOCOL: "Protocol",
    DOC_TYPE_UNKNOWN: "Uncertain",
}
# 回传归一（键一律小写去空格；中文别名一并接受）
_DOC_TYPE_ALIAS = {
    "原创研究": DOC_TYPE_ORIGINAL, "原创": DOC_TYPE_ORIGINAL,
    "original": DOC_TYPE_ORIGINAL, "research": DOC_TYPE_ORIGINAL,
    "rct": DOC_TYPE_ORIGINAL, "trial": DOC_TYPE_ORIGINAL,
    "综述": DOC_TYPE_REVIEW, "综述/meta": DOC_TYPE_REVIEW,
    "meta": DOC_TYPE_REVIEW, "meta-analysis": DOC_TYPE_REVIEW,
    "review": DOC_TYPE_REVIEW, "systematic review": DOC_TYPE_REVIEW,
    "指南": DOC_TYPE_GUIDELINE, "指南/共识": DOC_TYPE_GUIDELINE,
    "共识": DOC_TYPE_GUIDELINE, "guideline": DOC_TYPE_GUIDELINE,
    "consensus": DOC_TYPE_GUIDELINE,
    "研究方案": DOC_TYPE_PROTOCOL, "protocol": DOC_TYPE_PROTOCOL,
    "不确定": DOC_TYPE_UNKNOWN, "待确认": DOC_TYPE_UNKNOWN,
    "unknown": DOC_TYPE_UNKNOWN, "uncertain": DOC_TYPE_UNKNOWN,
}


def _norm_doc_type(v):
    """Excel 单元格 → internal 类型值。空值/无法识别返回 None（空值不覆盖规则预填）。"""
    if v is None:
        return None
    return _DOC_TYPE_ALIAS.get(str(v).strip().lower().replace(" ", ""))


def _bundled_skill_dir(skill_name):
    """载荷内置技能子集目录（发布沙箱运行时）；本机技能树布局下返回 None。

    发布载荷把跨技能运行时依赖放在 `<payload>/bundled/<skill>/`（见 workbench-dir
    `publish-kit/build_publish.py` 的 bundled 白名单）；`block_a.py` 位于
    `<payload>/adapters/`，故候选根为「adapters 的父目录」与「adapters 自身」。
    本机开发时该目录不在 adapters/ 同级 → 返回 None，调用方回落技能树真实路径。
    """
    here = os.path.dirname(os.path.abspath(__file__))
    for root in (os.path.dirname(here), here):
        cand = os.path.join(root, "bundled", skill_name)
        if os.path.isdir(cand):
            return cand
    return None


def _ct_scripts_dir():
    """ct-literature/scripts 绝对路径（跨技能懒加载；兼容 SkillHub 安装命名）。

    技能树优先（开发机）；沙箱内技能树不存在 → 回落载荷 bundled 子集（2026-09-17）。
    同一解析同时服务 doc_type_filter（文献类型预填）与 export_xlsx（合并表导出），
    它们的 import 在沙箱里同样曾因本机路径失配而静默走弱回退。
    """
    d = cc.resolve_skill_dir("~/.workbuddy/skills/ct-literature")
    if os.path.isdir(os.path.join(d, "scripts")):
        return os.path.join(d, "scripts")
    b = _bundled_skill_dir("ct-literature")
    if b:
        return os.path.join(b, "scripts")
    return os.path.join(d, "scripts")


def _kw_localize_scripts_dir():
    """kw_localize.py 所在目录：ct-base 权威 → ct-literature 同源副本 → 载荷 bundled。

    单一真源是 ct-base（ct-base 规范 bilingual_retrieval.md）；本机取权威版，沙箱
    回落到载荷已 bundled 的 ct-literature 副本（API 同源：localize_with_fallback /
    detect_lang 等 7 个公开函数一致，term_map 250 条 vs ct-base 254 条）。
    """
    cands = [_CT_BASE_SCRIPTS,
             os.path.join(cc.resolve_skill_dir("~/.workbuddy/skills/ct-base"), "scripts"),
             _ct_scripts_dir()]
    b = _bundled_skill_dir("ct-base")   # 若日后单独 bundled ct-base，自动优先于副本
    if b:
        cands.insert(2, os.path.join(b, "scripts"))
    for d in cands:
        if os.path.isfile(os.path.join(d, "kw_localize.py")):
            return d
    return cands[0]


def rule_doc_type(study):
    """规则预填文献类型（确定性、只读既有信号；**不引入第二套判定规则**）。

    单一真源：ct-literature 的 doc_type_filter.classify_record
    （pubType 元数据 + 声明短语 + head 词典三通道打分，平票降 unknown）。
    该模块不可用时回退到本技能既有的 is_likely_review()（pubType 硬信号 + 强短语），
    语义同族、不新增规则。

    返回 (doc_type, source)。source ∈ {"classify_record", "is_likely_review", "default"}，
    供导出表与审计追溯「这个预填值是怎么来的」。unknown 表示规则无从判 → 明确交人工。
    """
    s = study if isinstance(study, dict) else {}
    try:
        _d = _ct_scripts_dir()
        if _d not in sys.path:
            sys.path.insert(0, _d)
        import doc_type_filter as _dtf  # 懒加载；import 失败走回退
        cls = _dtf.classify_record(
            str(s.get("title") or ""),
            str(s.get("abstract_snippet") or s.get("abstract") or ""),
            s.get("pub_types")) or {}
        t = cls.get("type")
        if t in DOC_TYPE_ORDER:
            return t, "classify_record"
    except Exception:  # noqa: BLE001 — 跨技能模块不可用绝不阻断预填
        pass
    is_rev, rev_reason = is_likely_review(s)
    if is_rev:
        rs = str(rev_reason or "")
        if "指南" in rs or "共识" in rs:
            return DOC_TYPE_GUIDELINE, "is_likely_review"
        return DOC_TYPE_REVIEW, "is_likely_review"
    # 无标题/摘要可判 → 不猜，交人工确认
    if not (s.get("title") or s.get("abstract_snippet") or s.get("abstract")):
        return DOC_TYPE_UNKNOWN, "default"
    return DOC_TYPE_ORIGINAL, "default"


# ---------------------------------------------------------------------------
# A3 决策三态（include / exclude / uncertain）
# 后台原本只有 bool include，「低置信」靠 reason 里含「待人工」隐式表达，
# 前台无法按三态筛选。此处显式化，同时保留 include 布尔以兼容下游
# （A4 用 sc.get("include", True) 判定 → uncertain 一律 include=True，
#   维持「低置信宽松默认纳入、待人工确认」的既有语义，下游行为零变化）。
DECISION_INCLUDE = "include"
DECISION_EXCLUDE = "exclude"
DECISION_UNCERTAIN = "uncertain"


def decision_of(entry):
    """从一条 screened 记录推导三态决策（人工显式 decision 优先，否则按
    include + reason 推导）。返回 include/exclude/uncertain 之一。"""
    if not isinstance(entry, dict):
        return DECISION_UNCERTAIN
    d = entry.get("decision")
    if d in (DECISION_INCLUDE, DECISION_EXCLUDE, DECISION_UNCERTAIN):
        return d
    reason = entry.get("reason") or ""
    if "待人工" in reason:          # 未命中纳入关键词 / 默认纳入待确认
        return DECISION_UNCERTAIN
    return DECISION_INCLUDE if entry.get("include") else DECISION_EXCLUDE


# A3 逐条决策要展示的元数据字段（全部来自 ct-literature work，缺值为 None）。
# 集中定义，供 a3_screening / _a3_nha_from_screened 复用，避免两处漂移。
_A3_META_KEYS = ("journal", "authors", "publication_date", "volume", "issue",
                 "page", "study_type", "type", "cited_by_count", "keywords",
                 "relevance_score", "language", "is_safety", "pmid",
                 "abstract_snippet", "year", "doi", "source", "url",
                 "is_retracted")

# 字段别名：studies 有两条来源（coze result 直返 / _read_literature_dir 读文件），
# 同一含义的键名可能不同（如刊名 work 里叫 publication，归一化后叫 journal）。
# 按顺序取第一个非空值，保证两条路径展示一致，不会出现「有的行有刊名、有的没有」。
_A3_META_ALIASES = {
    "journal": ("journal", "publication", "venue", "journal_name"),
    "page": ("page", "pages"),
    "year": ("year", "publication_year"),
}


def _a3_meta(s):
    """从一条 study / screened 记录抽取 A3 决策所需元数据（含别名归一）。"""
    if not isinstance(s, dict):
        return {}
    out = {}
    for k in _A3_META_KEYS:
        for name in _A3_META_ALIASES.get(k, (k,)):
            v = s.get(name)
            if v is not None:
                out[k] = v
                break
    return out


def _a3_decision_row(s):
    """screened 记录 → 前台「逐条决策」一行（三态 + 元数据）。"""
    d = decision_of(s)
    # review-guard：优先用已存标记；Excel 回写重建的 screened 可能无该字段，
    # 此时从条目本身（标题/摘要）回退重算，保证徽标一致。
    is_rev = bool(s.get("is_review"))
    rev_reason = s.get("review_reason")
    if not is_rev and (s.get("title") or s.get("abstract_snippet")):
        is_rev, rev_reason = is_likely_review(s)
    row = {
        "title": s.get("title"),
        "decision": d,
        # 兼容字段：uncertain 视为宽松纳入（与既有下游语义一致）
        "include": d != DECISION_EXCLUDE,
        "reason": s.get("reason"),
        # review-guard：标记疑似综述/meta，供前台打黄标提醒人工复核
        "is_review": is_rev,
        "review_reason": rev_reason,
        # 文献类型（权威值）：Excel 回传重建的 screened 可能无该字段 → 规则回退预填，
        # 保证前台/导出/A4 三处读到同一值，绝不出现"有的行有类型、有的没有"。
        "doc_type": s.get("doc_type") or rule_doc_type(s)[0],
        "doc_type_source": s.get("doc_type_source") or "rule",
    }
    row.update(_a3_meta(s))
    return row


def a3_screening(studies, inclusion_hints=None):
    seen = set()
    screened = []
    for s in studies:
        if not isinstance(s, dict):
            continue
        key = (str(s.get("doi") or s.get("title") or "").strip().lower())
        if not key or key in seen:
            continue
        seen.add(key)
        inc, reason = _heuristic_include(s, inclusion_hints)
        is_rev, rev_reason = is_likely_review(s)
        if is_rev and inc:
            # review-guard：命中综述特征 → 默认排除（从源头不送 A4 抽取，综述本无原始 2×2）。
            # 只降不升：已被启发式剔除的保持其更严的排除理由；人工可在裁决下拉翻回「纳入」
            # （decision_of 显式 decision 优先，翻回即生效），故这是"默认排除"而非硬锁。
            inc = False
            reason = f"review-guard 默认排除：{rev_reason}（如确需此综述请在裁决中翻为纳入）"
        # 文献类型：规则预填（确定性，单一真源见 rule_doc_type），人工在裁决表确认后
        # 该字段成为权威值；A4 只读，不再自行判定类型。
        dt, dt_src = rule_doc_type(s)
        entry = {
            "title": s.get("title"),
            "year": s.get("year"),
            "doi": s.get("doi"),
            "include": inc,
            "reason": reason,
            # review-guard：疑似综述标记（供前台黄徽标 + 默认排除依据，人工裁决优先）
            "is_review": is_rev,
            "review_reason": rev_reason,
            # 规则预填的文献类型（original|review|guideline|protocol|unknown）
            "doc_type": dt,
            "doc_type_source": dt_src,
            # 透传摘要片段，供人工/下载决策判断"是否真相关"
            "abstract_snippet": s.get("abstract_snippet"),
        }
        # 人工裁决所需元数据：刊名/作者/卷期页/研究类型等一并留存
        # （_a3_meta 统一处理两条数据来源的键名差异，见其注释）
        entry.update(_a3_meta(s))
        screened.append(entry)
    return screened, _a3_nha_from_screened(screened)


def _a3_nha_from_screened(screened):
    """从（人工修订后的）screened 列表重建 A3 的 next_human_action 载荷，
    供 override_screened 路径复用（不重跑启发式，避免覆盖人工裁决）。

    三态口径：include / exclude / uncertain，逐条由 decision_of() 推导
    （人工显式 decision 优先）。uncertain = 待人工核验相关性。
    """
    screened = [s for s in (screened or []) if isinstance(s, dict)]
    decs = [decision_of(s) for s in screened]
    n_inc = decs.count(DECISION_INCLUDE)
    n_exc = decs.count(DECISION_EXCLUDE)
    n_uncertain = decs.count(DECISION_UNCERTAIN)
    # review-guard：命中综述特征且被默认排除的篇数（供提示语说明"为何自动剔除"）
    n_rev_excl = sum(1 for s in screened
                     if s.get("is_review") and decision_of(s) == DECISION_EXCLUDE)
    # 文献类型分布（权威值 = 人工确认值优先，缺席则规则预填）——供菜单展示与审计
    ty_dist = {}
    for s in screened:
        t = s.get("doc_type") or rule_doc_type(s)[0]
        ty_dist[t] = ty_dist.get(t, 0) + 1
    n_type_unconfirmed = sum(1 for s in screened
                             if (s.get("doc_type_source") or "rule") == "rule")
    rev_note = (f"其中 {n_rev_excl} 篇疑似综述（review/meta）已被默认排除——综述无原始 2×2 数据，"
                f"如确需保留请在对应行翻为「纳入」；"
                if n_rev_excl else "")
    return {
        "type": "review",
        "prompt": (f"初筛裁决（软停）：去重后 {len(screened)} 篇，"
                   f"纳入 {n_inc} / 剔除 {n_exc} / 低置信 {n_uncertain}。"
                   f"{rev_note}"
                   f"低置信需人工定夺（默认随纳入走，但请复核）。"
                   f"请逐条确认或翻转，重点复核剔除项以防误剔关键研究。"),
        "required": True,
        "gate": "none",
        "summary": {"n_total": len(screened), "n_include": n_inc,
                    "n_exclude": n_exc, "n_uncertain": n_uncertain,
                    "n_review_excluded": n_rev_excl,
                    # 文献类型分布（权威值）+ 未在裁决表确认的篇数（空白单元格）
                    "doc_type_dist": ty_dist,
                    "n_type_unconfirmed": n_type_unconfirmed},
        "decisions": [_a3_decision_row(s) for s in screened],
    }


# ---------------------------------------------------------------------------
# A3 裁决表 Excel 导入/导出（复用 ct-literature 既有模板，不重造）
# ---------------------------------------------------------------------------
def _match_key(doi, title):
    """归一化匹配键（单键）：DOI 优先，缺则回退归一化标题。与 ct-literature
    export_xlsx._norm_doi/_norm_title 口径一致。供导出侧单键 attach 用。"""
    if doi:
        return ("doi", str(doi).strip().lower())
    if title:
        return ("title", " ".join(str(title).strip().lower().split()))
    return None


def _match_keys(doi, title):
    """归一化匹配键（多键列表）：DOI 与标题各自独立成键。

    上传解析时 works 表可能只暴露「标题」（早期模板无 DOI 列），而基线
    decisions 带 DOI —— 两套键空间若不相交会 matched=0。改为任一键命中即
    匹配，彻底消除该问题。
    """
    keys = []
    if doi:
        keys.append(("doi", str(doi).strip().lower()))
    if title:
        keys.append(("title", " ".join(str(title).strip().lower().split())))
    return keys


_DECISION_ALIAS = {
    "纳入": "include", "包含": "include", "in": "include", "include": "include",
    "剔除": "exclude", "排除": "exclude", "ex": "exclude", "exclude": "exclude",
    "低置信": "uncertain", "不确定": "uncertain", "un": "uncertain",
    "uncertain": "uncertain",
}


def _norm_decision(v):
    """把 Excel 单元格里的裁决值归一为 include/exclude/uncertain，无法识别返回 None。"""
    if v is None:
        return None
    return _DECISION_ALIAS.get(str(v).strip())


def _hdr_idx(idx, names):
    for n in names:
        if n in idx:
            return idx[n]
    return None


def _load_merged_works(session_dir):
    """递归找 .merged.json，返回其 works[]（ct-literature 全字段底表）。"""
    session_dir = os.path.abspath(session_dir)
    import glob
    candidates = [os.path.join(session_dir, ".merged.json")]
    candidates += sorted(glob.glob(os.path.join(session_dir, "**", ".merged.json"),
                                   recursive=True))
    for p in candidates:
        if os.path.isfile(p):
            try:
                d = json.load(open(p, encoding="utf-8"))
                ws = d.get("works") or []
                if ws:
                    return ws
            except Exception:  # noqa: BLE001
                continue
    return []


def _doc_type_cell_for_export(work, decision, lang="zh"):
    """导出表「文献类型确认」列的预填单元格值（显示标签，人工可读）。

    优先级：work 全字段过规则（含 pub_types，信号最全）→ decision 已存 doc_type
    （A3 阶段算好的）→ 规则回退。unknown 照实写「不确定」，明确交人工定夺——
    预填空着等于让用户从零填，规则就白跑了。
    """
    src = work if isinstance(work, dict) else {}
    d = decision if isinstance(decision, dict) else {}
    dt = rule_doc_type(src)[0] if src else DOC_TYPE_UNKNOWN
    if dt == DOC_TYPE_UNKNOWN:
        _dt_d = d.get("doc_type")
        if _dt_d in DOC_TYPE_ORDER and _dt_d != DOC_TYPE_UNKNOWN:
            dt = _dt_d
    labels = DOC_TYPE_LABELS_EN if str(lang).startswith("en") else DOC_TYPE_LABELS
    return labels.get(dt) or labels[DOC_TYPE_UNKNOWN]


def export_screening_xlsx(session_path, out_path, lang="zh"):
    """导出**合并节点（A2「文献集」）**为一张 xlsx：检索结果 + 裁决/理由/文献类型确认列。

    用户裁定（2026-09-10）：A2 检索 与 A3 初筛合并 → **单节点、单表**。底表取 A2
    `stage_result.studies`（**本会话当次检索结果**，权威），**不读**共享的
    `.merged.json`（同目录多会话共用、会被后跑覆盖，易张冠李戴）；叠加本节点
    `nha.decisions` 的「裁决/理由」与规则预填的「文献类型确认」列。

    复用 ct-literature/scripts/export_xlsx（用户指定的「原先设计好的 excel」），
    不重造模板。返回 (out_path, n_works)。
    """
    from fullflow import FullflowSession
    sess = FullflowSession.load(session_path)
    st = _a2_stage_of(sess)
    sr = (st or {}).get("stage_result") or {}
    nha = (st or {}).get("next_human_action") or {}
    decisions = nha.get("decisions") or []
    if not decisions:
        # 兼容旧会话（A2/A3 尚未合并）：decisions 仍挂在 A3 阶段的 await 载荷上
        await_blk = ((sess.data.get("last_view") or {}).get("fullflow") or {}).get("await") or {}
        if await_blk.get("stage_id") == A3_LEGACY:
            decisions = (await_blk.get("nha") or {}).get("decisions") or []
    if not decisions:
        raise ValueError("当前会话无裁决数据（decisions 为空），无法导出合并表")
    # 底表 works = 本会话 A2 检索结果（含摘要/作者/刊名等全字段），按 doi/title 匹配 decisions
    works = sr.get("studies") or []
    if not works:
        await_blk = ((sess.data.get("last_view") or {}).get("fullflow") or {}).get("await") or {}
        works = ((await_blk.get("stage_result") or {}).get("studies")) or []
    dec_by_key = {}
    for d in decisions:
        k = _match_key(d.get("doi"), d.get("title"))
        if k:
            dec_by_key[k] = d
    ct_decisions = []
    used = set()
    for w in works:
        k = _match_key(w.get("doi"), w.get("title"))
        if k and k in dec_by_key and k not in used:
            used.add(k)
            d = dec_by_key[k]
            ct_decisions.append({
                "title": w.get("title"),
                "doi": w.get("doi"),
                "decision": d.get("decision") or decision_of(d),
                "reason": d.get("reason") or "",
                # 文献类型预填：以底层 work 全字段（含 pub_types）过规则；规则无从判
                # （unknown）而 A3 已有值时沿用 A3 值，绝不留空让人重填。
                "doc_type": _doc_type_cell_for_export(w, d, lang),
            })
    # 兜底：底表为空或匹配不到时，直接以 decisions 为 works（至少能导出裁决）
    if not ct_decisions:
        ct_decisions = [{"title": d.get("title"), "doi": d.get("doi"),
                         "decision": d.get("decision") or decision_of(d),
                         "reason": d.get("reason") or "",
                         "doc_type": _doc_type_cell_for_export(None, d, lang)}
                        for d in decisions]
        works = [{"title": d.get("title"), "doi": d.get("doi")} for d in decisions]
    # 懒加载 ct-literature 导出模块（不硬依赖，跨技能复用）
    # 兼容 SkillHub 安装命名（ct-literature__skillhub）：经 cc.resolve_skill_dir 解析。
    _ct = _ct_scripts_dir()
    if _ct not in sys.path:
        sys.path.insert(0, _ct)
    import export_xlsx as ex  # noqa: F401  (懒加载；import 失败即抛，由端点捕获)
    cov = nha.get("coverage") or sr.get("coverage") or {}
    meta = {"topic": sess.data.get("topic", ""), "total": len(works),
            "query": cov.get("translated_query") or cov.get("query"),
            "by_source": cov.get("by_source"),
            "search_status": cov.get("search_status"),
            "max_results": cov.get("max_results"),
            "year_from": cov.get("year_from"),
            "stage": A2}
    # 裁决列下拉选项：中文显示标签 + 英文 internal 值，与 _DECISION_ALIAS 口径
    # 一致（parse_screening_xlsx 经 _norm_decision 归一）。双标签兼容预填英文值。
    decision_options = ["纳入", "排除", "低置信", "include", "exclude", "uncertain"]
    # 附加列「文献类型确认」（D17-A）：规则预填 → 人工在此列确认/改判 → 回传成
    # 权威 doc_type，A4 只读。扩展位在 ct-literature export_xlsx 侧（通用、向后兼容）。
    doc_type_options = (list(DOC_TYPE_LABELS.values())
                        + list(DOC_TYPE_LABELS_EN.values())
                        + list(DOC_TYPE_ORDER))
    decision_extra = [{
        "key": "doc_type",
        "label": "col.doc_type_confirmed",
        "width": 16,
        "options": doc_type_options,
        "error_message": "请从下拉选择文献类型：原创研究 / 综述·Meta / 指南·共识 / 研究方案 / 不确定",
    }]
    ex.export_workbook({"count": len(works), "works": works, "meta": meta},
                       out_path, lang=lang, decisions=ct_decisions,
                       decision_options=decision_options,
                       decision_extra=decision_extra)
    return out_path, len(works)


def _a2_stage_of(sess):
    """取 A 块信封里的 A2 stage 条目（无则 None）。"""
    env = ((sess.data.get("blocks") or {}).get("A") or {}).get("envelope") or {}
    for st in env.get("stages") or []:
        if (st.get("stage") or {}).get("id") == A2:
            return st
    return None


def _a2_payload_of(sess):
    """返回 (studies, coverage)：A2 的检索结果与覆盖信息。"""
    st = _a2_stage_of(sess)
    if not st:
        return [], {}
    sr = st.get("stage_result") or {}
    nha = st.get("next_human_action") or {}
    return (sr.get("studies") or []), (nha.get("coverage") or sr.get("coverage") or {})


def _a3_legacy_guard(sess):
    """旧会话兼容：A2/A3 合并前，A3 阶段的 await 载荷仍可能持有 screened/decisions。"""
    await_blk = ((sess.data.get("last_view") or {}).get("fullflow") or {}).get("await") or {}
    return await_blk if await_blk.get("stage_id") == A3_LEGACY else {}


def parse_screening_xlsx(xlsx_path, current_decisions):
    """解析上传的裁决表（ct-literature 模板，含裁决/理由/文献类型确认列）。

    以 current_decisions 为基线（保留元数据），按 DOI/标题匹配覆盖「裁决/理由/
    文献类型」。类型列非空即视为**人工确认值**（权威），并留下 doc_type_rule
    作规则预填的对照，供审计「人工改判了几篇」；列空则沿用基线规则预填。
    非法类型值（既非下拉标签也非 internal 值）→ 直接报错，不前进。

    返回 (screened, stats)。stats: {matched, updated, unmatched, total,
    type_confirmed, type_changed, type_blank}。
    screened 为完整决策行列表（含元数据 + include 派生），可直接喂 override_screened。
    """
    import openpyxl
    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    # 优先找含「裁决」表头的 sheet
    target = None
    for ws in wb.worksheets:
        rows = ws.iter_rows(values_only=True)
        try:
            hdr = next(rows)
        except StopIteration:
            continue
        if hdr and any(isinstance(h, str) and "裁决" in h for h in hdr):
            target = (hdr, rows)
            break
    if target is None and wb.worksheets:
        ws = wb.worksheets[0]
        rows = ws.iter_rows(values_only=True)
        hdr = next(rows)
        target = (hdr, rows)
    if target is None:
        raise ValueError("上传的 xlsx 无工作表")
    hdr, rows = target
    idx = {str(h).strip(): i for i, h in enumerate(hdr) if h is not None}
    i_doi = _hdr_idx(idx, ["doi", "DOI", "DOI/PMID"])
    i_title = _hdr_idx(idx, ["标题", "title", "Title"])
    i_dec = _hdr_idx(idx, ["裁决", "决策", "decision", "Decision"])
    i_reason = _hdr_idx(idx, ["理由", "reason", "Reason"])
    # 文献类型确认列（D17-A）：旧版模板可能没有 → 缺席即视为"未确认"，
    # 沿用基线规则预填，不报错（向后兼容旧导出表）。
    i_dtype = _hdr_idx(idx, ["文献类型确认", "类型确认", "Confirmed type",
                             "doc_type", "doc type"])
    # 上传表：每个单元格行按 DOI/标题各生成一个匹配键（多键）→ (decision, reason)
    # 用 _match_keys 而非 _match_key：早期模板若无 DOI 列、仅标题，仍能与带 DOI
    # 的基线 decisions 命中，杜绝「两套键空间不相交 → matched=0」。
    upload_by_key = {}
    bad_types = []
    for r in rows:
        if r is None:
            continue
        doi = r[i_doi] if (i_doi is not None and i_doi < len(r)) else None
        title = r[i_title] if (i_title is not None and i_title < len(r)) else None
        dec_raw = r[i_dec] if (i_dec is not None and i_dec < len(r)) else None
        reason = r[i_reason] if (i_reason is not None and i_reason < len(r)) else None
        dt_raw = r[i_dtype] if (i_dtype is not None and i_dtype < len(r)) else None
        dt_txt = "" if dt_raw is None else str(dt_raw).strip()
        dt_val = _norm_doc_type(dt_raw)
        # 非空但认不出 → 记下（含行定位），最终一次性报错，不静默当"未填"
        if dt_txt and dt_val is None:
            bad_types.append({
                "title": ("" if title is None else str(title))[:60],
                "doi": "" if doi is None else str(doi),
                "value": dt_txt})
        val = {"decision": _norm_decision(dec_raw),
               "reason": "" if reason is None else str(reason).strip(),
               # None = 单元格空 → 未确认（沿用基线）；否则为人工确认值
               "doc_type": dt_val,
               "doc_type_raw": dt_txt}
        for k in _match_keys(doi, title):
            upload_by_key[k] = val
    if bad_types:
        _ex = "；".join(f"第{i + 1}处「{b['title']}」= {b['value']}"
                        for i, b in enumerate(bad_types[:5]))
        raise ValueError(
            "文献类型列存在无法识别的取值（%d 处）：%s。"
            "请从下拉选择：原创研究 / 综述·Meta / 指南·共识 / 研究方案 / 不确定"
            "（或留空＝沿用规则预填）" % (len(bad_types), _ex))
    # 合并：基线（保留元数据）+ 上传覆盖裁决/理由；基线任一匹配键命中即视为匹配
    screened = []
    n_matched = n_updated = 0
    n_type_confirmed = n_type_changed = n_type_blank = 0
    base_keys = set()
    for d in current_decisions:
        base_keys.update(_match_keys(d.get("doi"), d.get("title")))
    for d in current_decisions:
        entry = dict(d)
        hit = None
        for k in _match_keys(d.get("doi"), d.get("title")):
            if k in upload_by_key:
                hit = upload_by_key[k]
                break
        if hit is not None:
            n_matched += 1
            if hit["decision"] and hit["decision"] != entry.get("decision"):
                entry["decision"] = hit["decision"]
                n_updated += 1
            if hit["reason"]:
                entry["reason"] = hit["reason"]
            # 文献类型：表内非空 = 人工确认值（权威）。留 doc_type_rule 作规则预填
            # 的对照 → 可审计「人工改判了几篇」，也便于回溯规则是否偏了。
            rule_val = entry.get("doc_type") or rule_doc_type(entry)[0]
            entry["doc_type_rule"] = rule_val
            if hit.get("doc_type"):
                entry["doc_type"] = hit["doc_type"]
                entry["doc_type_source"] = "human"
                entry["doc_type_confirmed"] = True
                n_type_confirmed += 1
                if hit["doc_type"] != rule_val:
                    entry["doc_type_changed"] = True
                    n_type_changed += 1
            else:
                # 单元格留空 = 未确认 → 沿用规则预填（不拦流程，但要看得见）
                entry["doc_type"] = rule_val
                entry["doc_type_source"] = "rule"
                entry["doc_type_confirmed"] = False
                n_type_blank += 1
        else:
            # 上传表未覆盖到的基线行：类型保持规则预填，标记未确认
            entry["doc_type"] = entry.get("doc_type") or rule_doc_type(entry)[0]
            entry["doc_type_source"] = entry.get("doc_type_source") or "rule"
            entry["doc_type_confirmed"] = False
        screened.append(entry)
    # 规整：补 include 派生字段（下游语义：uncertain/exclude 均按需）
    for s in screened:
        s["include"] = decision_of(s) != DECISION_EXCLUDE
    unmatched = sum(1 for k in upload_by_key if k not in base_keys)
    # 整表零匹配 = 上传的不是本会话的裁决表，或标题/DOI 列被改动导致键空间不相交。
    # 报错不前进：静默 matched=0 会让用户以为"改完了、已生效"，实际一条都没回写。
    if screened and n_matched == 0:
        raise ValueError(
            "上传表与当前裁决清单无任何匹配（0/%d）：可能上传了其他会话的裁决表，"
            "或「标题 / DOI」列被改动。请确认后重新上传。" % len(screened))
    stats = {"matched": n_matched, "updated": n_updated,
             "unmatched": unmatched, "total": len(screened),
             "type_confirmed": n_type_confirmed, "type_changed": n_type_changed,
             "type_blank": n_type_blank,
             # DOI 列是否存在（旧模板无此列时回退标题匹配，可见性优于猜测）
             "doi_column": i_doi is not None}
    return screened, stats


def apply_screening_upload(session_path, screened):
    """把上传解析后的裁决应用到当前会话（合并节点 A2「文献集」）：
    1) 更新该节点软停快照的 decisions（对话菜单 / 前端立即可见）；
    2) 记录一条 revised 决策（sticky：后续 approved 经 override_screened 生效）。
    不前进流程，回到该节点软停供复核。返回更新后的 FullflowSession。

    兼容旧会话：A2/A3 合并前快照可能停在 A3.screening —— 此时按 A3 处理。
    """
    from fullflow import FullflowSession
    sess = FullflowSession.load(session_path)
    # 工作台读取的 canonical 位置是 last_view.fullflow.await（与 build_state 同源）；
    # data["await"] 作为兼容位置一并更新，避免两处漂移。
    lv_await = (((sess.data.get("last_view") or {}).get("fullflow") or {}).get("await") or {})
    legacy_await = sess.data.get("await") or {}
    sid = lv_await.get("stage_id") or legacy_await.get("stage_id")
    if sid not in (A2, A3_LEGACY):
        raise ValueError("当前不在文献集节点（A2），无法应用 Excel 上传（stage_id=%s）" % sid)
    base_nha = lv_await.get("nha") or legacy_await.get("nha") or {}
    if sid == A2:
        # 合并节点：只替换裁决段，保留原检索覆盖段（coverage / search_strategy）
        _sn = _a3_nha_from_screened(screened)
        new_nha = {**base_nha, "summary": _sn.get("summary") or {},
                   "decisions": _sn.get("decisions") or []}
    else:
        new_nha = _a3_nha_from_screened(screened)
    # 与 export_screening_xlsx / build_state 同源：nha 是 await 的顶层键（与 stage_result 并列）
    if lv_await:
        lv_await["nha"] = new_nha
        sess.data["last_view"]["fullflow"]["await"] = lv_await
    if legacy_await:
        legacy_await["nha"] = new_nha
        sess.data["await"] = legacy_await
    # 同步写回阶段快照的 screened，保证下游 A4 与 Excel 导出读到同一份裁决
    env = ((sess.data.get("blocks") or {}).get("A") or {}).get("envelope") or {}
    for st in env.get("stages") or []:
        if (st.get("stage") or {}).get("id") == sid:
            sr = st.setdefault("stage_result", {})
            sr["screened"] = screened
            sr["n_screened"] = len(screened)
    sess.record_decision({
        "stage_id": sid, "action": "revised",
        "revision": {"screened": screened},
        "note": "Excel 上传更新裁决", "decided_by": "workbench",
    })
    sess.save()
    return sess


# ---------------------------------------------------------------------------
# A4 提取 + 🔴 extraction_review 红线闸（本地强执）
# ---------------------------------------------------------------------------
def _parse_extraction(extraction_table):
    if isinstance(extraction_table, list):
        return extraction_table
    if isinstance(extraction_table, str) and extraction_table.strip():
        try:
            return json.loads(extraction_table)
        except json.JSONDecodeError:
            # 退化：按行拆分，标记待结构化
            return [{"raw": ln} for ln in extraction_table.strip().splitlines() if ln.strip()]
    return []


# ---------------------------------------------------------------------------
# 工作台「我已备好原始数据」快速通道：CSV / Excel → extracted_rows
# ---------------------------------------------------------------------------
def parse_raw_csv(path, text=None):
    """解析用户自备的原始数据表（CSV / .xlsx / .xls，或直接粘贴的 text）为 Block B 可直接消费的
    extracted_rows（规范化字段 ai/bi/ci/di 或 te/sete + study）。

    支持中英文列名，兼容两种 2×2 布局：
      - 事件/非事件布局：ai=实验组事件, bi=实验组非事件, ci=对照组事件, di=对照组非事件
        （与 pdf_extractor / _norm_b1_rows 一致：n_exp = ai+bi）
      - 事件/总数布局：ai=实验组事件, bi=实验组总数（含事件）… 此时自动换算 bi = 总数 - ai
    亦支持预计算效应量列 te / sete（效力量直接进 B1 合并）。
    无 pandas 时退化到标准库 csv（仅支持 .csv）。返回 list[dict]。
    """
    low = str(path).lower()
    df = None
    try:
        import pandas as pd  # 懒加载：仅 fast-path 用，缺失不影响主流程
        if text is not None:
            import io as _io
            df = pd.read_csv(_io.StringIO(text), sep=None, engine="python")
        elif low.endswith((".xlsx", ".xls")):
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)
    except Exception:
        import csv as _csv, io as _io
        if text is not None:
            df = list(_csv.DictReader(_io.StringIO(text)))
        else:
            with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
                df = list(_csv.DictReader(f))
    if df is None:
        return []

    # 列名标准化（小写、去空格）映射
    if isinstance(df, list):
        cols = {str(c).strip().lower(): c for c in (df[0].keys() if df else [])}
        rows_in = df
    else:
        cols = {str(c).strip().lower(): c for c in df.columns}
        rows_in = df.to_dict(orient="records")

    def _pick(*names):
        for n in names:
            if n in cols:
                return cols[n]
        return None

    study_c = _pick("study", "stid", "slab", "label", "study_id", "研究", "研究名称", "文献", "标题")
    # 试验组 / 实验组 两种写法都兼容（临床试验常用「试验组」，实验学科常用「实验组」）
    ai_c = _pick("ai", "a_e", "event_e", "trt_event", "events_exp",
                 "试验组事件", "事件_试验", "实验组事件", "事件_实验")
    bi_c = _pick("bi", "b_e", "nonevent_e", "n_e", "sample_e", "total_e", "trt_n", "n_exp",
                 "试验组样本", "试验组总数", "试验组样本量", "样本_试验", "试验组非事件", "非事件_试验",
                 "实验组样本", "实验组总数", "实验组样本量", "样本_实验",
                 "实验组非事件", "非事件_实验")
    ci_c = _pick("ci", "c_e", "event_c", "ctrl_event", "事件_对照", "对照组事件")
    di_c = _pick("di", "d_e", "nonevent_c", "n_c", "sample_c", "total_c", "ctrl_n", "n_ctrl",
                 "对照组样本", "样本_对照", "对照组总数", "对照组样本量",
                 "对照组非事件", "非事件_对照")
    te_c = _pick("te", "yi", "effect", "效应量", "对数效应量")
    se_c = _pick("sete", "sei", "se", "标准误", "标准误se")
    # ---- 连续结局（MD / SMD）：契约默认列 mean_exp/sd_exp/n_exp/mean_ctrl/sd_ctrl/n_ctrl ----
    # 2026-09-17 新增：此前只支持 2×2 与 te/sete，用户按 MD/SMD 自备「均值±标准差」表时
    # 无法解析（首页示例也就无从随效应量变化）。此处按名字归一，值原样产出交给 R 引擎
    # （escalc/metacont，sm=MD/SMD）—— block_b._norm_b1_rows 对未知列原样透传。
    import math as _m
    me_c = _pick("mean_exp", "mean_e", "meane", "mean1", "group1_mean",
                 "试验组均值", "实验组均值", "均值_试验", "均值_实验")
    sd1_c = _pick("sd_exp", "sd_e", "sde", "sd1", "group1_sd",
                  "试验组标准差", "实验组标准差", "标准差_试验", "标准差_实验")
    ne_c = _pick("n_exp", "n_e", "n1", "group1_n",
                 "试验组样本量", "实验组样本量", "样本量_试验", "样本量_实验")
    mc_c = _pick("mean_ctrl", "mean_c", "meanc", "mean2", "group2_mean", "对照组均值", "均值_对照")
    sd2_c = _pick("sd_ctrl", "sd_c", "sdc", "sd2", "group2_sd", "对照组标准差", "标准差_对照")
    nc_c = _pick("n_ctrl", "n_c", "n2", "group2_n", "对照组样本量", "样本量_对照")
    # ---- 生存结局（HR）：hr +（se | ci_low/ci_high）→ 换算为对数尺度 te/sete ----
    hr_c = _pick("hr", "hazard_ratio", "hr值", "风险比", "adj_hr", "hr_adj", "调整hr")
    loghr_c = _pick("loghr", "log_hr", "lnhr", "对数风险比")
    lo_c = _pick("ci_low", "ci_lower", "lower", "lower95", "ll", "lcl",
                 "下限", "ci下限", "95ci_low", "ci_low95", "ci_low_95")
    hi_c = _pick("ci_high", "ci_upper", "upper", "upper95", "ul", "ucl",
                 "上限", "ci上限", "95ci_high", "ci_high95", "ci_high_95")

    # bi/di 是否为「总数」而非「非事件」：列名含 total/n/样本/总数 → 总数布局
    def _is_total(colname):
        if not colname:
            return False
        return any(k in colname for k in ("total", "n_", "样本", "总数", "sample"))
    bi_is_total = _is_total(bi_c)
    di_is_total = _is_total(di_c)

    def _num(v):
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return float(v) if v == v else None
        s = str(v).strip().replace(",", "")
        if s == "":
            return None
        try:
            return float(s)
        except ValueError:
            return None

    out = []
    for i, r in enumerate(rows_in):
        study = str(r.get(study_c, "") or f"S{i + 1}").strip() or f"S{i + 1}"
        ai, ci = _num(r.get(ai_c)) if ai_c else None, _num(r.get(ci_c)) if ci_c else None
        bi, di = _num(r.get(bi_c)) if bi_c else None, _num(r.get(di_c)) if di_c else None
        te, se = _num(r.get(te_c)) if te_c else None, _num(r.get(se_c)) if se_c else None
        row = {"study": study}
        if ai is not None and ci is not None and bi is not None and di is not None:
            if bi_is_total:
                bi = bi - ai
            if di_is_total:
                di = di - ci
            if bi < 0 or di < 0:
                continue
            row.update({"ai": ai, "bi": bi, "ci": ci, "di": di})
            out.append(row)
        elif (me_c and sd1_c and ne_c and mc_c and sd2_c and nc_c
              and all(_num(r.get(c)) is not None
                      for c in (me_c, sd1_c, ne_c, mc_c, sd2_c, nc_c))):
            # 连续结局（MD / SMD）：按契约默认列名产出，交给 R 引擎
            row.update({
                "mean_exp": _num(r.get(me_c)), "sd_exp": _num(r.get(sd1_c)),
                "n_exp": _num(r.get(ne_c)),
                "mean_ctrl": _num(r.get(mc_c)), "sd_ctrl": _num(r.get(sd2_c)),
                "n_ctrl": _num(r.get(nc_c)),
            })
            out.append(row)
        elif hr_c and _num(r.get(hr_c)) and _num(r.get(hr_c)) > 0:
            # 生存结局（HR）：换算到对数尺度 TE=ln(HR)；SE 优先用显式 se/sete，
            # 否则由 95% CI 反推（SE = (ln UL − ln LL) / 2·1.96）。
            hr_v = _num(r.get(hr_c))
            se_v = _num(r.get(se_c)) if se_c else None
            lo_v = _num(r.get(lo_c)) if lo_c else None
            hi_v = _num(r.get(hi_c)) if hi_c else None
            if se_v is None and lo_v and hi_v and lo_v > 0 and hi_v > lo_v:
                se_v = (_m.log(hi_v) - _m.log(lo_v)) / (2 * 1.959964)
            if se_v and se_v > 0:
                row.update({"te": _m.log(hr_v), "sete": se_v, "hr": hr_v})
                out.append(row)
        elif (loghr_c and _num(r.get(loghr_c)) is not None
              and se_c and _num(r.get(se_c)) is not None):
            # 已给「对数 HR + 标准误」的表格：直接透传
            row.update({"te": _num(r.get(loghr_c)), "sete": _num(r.get(se_c))})
            out.append(row)
        elif te is not None and se is not None:
            row.update({"te": te, "sete": se})
            out.append(row)
    return out


def a4_seed_from_pdfs(pdf_paths, pdf_dir=None):
    """从用户上传的若干 PDF 直接抽取 2×2 表，构造 A4 结果（含逐篇 per_doc）。

    供工作台「我已备好全文 PDF」快速通道：把上传的 PDF 落盘到 A4 缓存目录后，
    用与 a4_stream 相同的 pdf_extractor 抽取，返回与 a4_stream 同构的 a4_result
    （extracted_rows / per_doc / 计数）。缺 pdf_extractor 时优雅降级：PDF 仍落盘、
    per_doc 标 needs_upload 待人工补抽取。
    """
    try:
        import pdf_extractor  # noqa: F401
    except Exception:  # noqa: BLE001
        pdf_extractor = None
    if pdf_dir is None:
        pdf_dir = A4_PDF_CACHE_DIR
    os.makedirs(pdf_dir, exist_ok=True)

    per_doc, extracted_rows, review_rows, fetch_log = [], [], [], []
    total = len(pdf_paths)
    n_ext = 0
    for i, src in enumerate(pdf_paths):
        src = str(src)
        title = os.path.splitext(os.path.basename(src))[0] or f"doc{i + 1}"
        stem = "up_%d_%s" % (i + 1, re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", title)[:40].strip("_") or f"doc{i + 1}")
        dst = os.path.join(pdf_dir, stem + ".pdf")
        try:
            shutil.copyfile(src, dst)
        except Exception:  # noqa: BLE001
            dst = src  # 复制失败则直接用原路径（仍在本地）
        status, rows, reason, err, cands = "needs_upload", [], None, None, []
        doc_info = None
        if pdf_extractor is not None:
            rows, tworows, n_cand, err, cands, doc_info = _a4_extract_pdf(dst, pdf_extractor)
            # 类型一律不作门（2026-09-10）：人工已确认文献类型，此处只抽取 + 标注。
            # doc_info.type_notice 是给 🔴 闸位的**提示**，不是排除依据。
            tworows = [r for r in rows if all(r.get(k) is not None for k in ("ai", "bi", "ci", "di"))]
            eff_rows = [dict(r, TE=r.get("te"), seTE=r.get("sete")) for r in rows
                        if r.get("te") is not None and r.get("sete") is not None
                        and str(r.get("anchor") or "").startswith("p")
                        and "table#" in str(r.get("anchor") or "")]
            extracted_rows.extend(tworows)
            extracted_rows.extend(eff_rows)
            review_rows.extend(rows)
            n_ext += len(tworows) + len(eff_rows)
            if err:
                reason = "PDF 抽取失败：%s" % err
            else:
                # 无错误时，把类型提示当 reason 透出（供闸位提示，非排除）
                reason = (doc_info or {}).get("type_notice") or None
            status = "extracted"
            fetch_log.append({"title": title, "pdf": dst, "n_rows": len(rows),
                              "n_tworows": len(tworows),
                              "doc_type": (doc_info or {}).get("type"),
                              "gate": "pass_uploaded"})
        else:
            reason = "pdf_extractor 不可用（缺 fitz/pdfplumber），PDF 已落盘待补抽取"
        per_doc.append({
            "index": i, "title": title, "doi": None, "status": status,
            "reason": reason, "pdf": dst, "rows": rows, "candidates": cands,
            "n_rows": len(rows), "n_tworows": len([r for r in rows
                if all(r.get(k) is not None for k in ("ai", "bi", "ci", "di"))]),
            # 人工直传 PDF 路径无 A3 记录可读 → 只能给抽取层探测值，并**明确标注
            # 来源为 detected**（提示词）。A4 不做类型判断，也不据此排除任何文献。
            "doc_type": (doc_info or {}).get("type"),
            "doc_type_detected": (doc_info or {}).get("type"),
            "doc_type_confirmed": None,
            "doc_type_source": "detected",
            # 类型不再产生任何排除：是否真正纳入由 A3 裁决表决定
            "included": True,
            "is_review": bool((doc_info or {}).get("type") in DOC_TYPE_NO_PRIMARY),
        })
    return {
        "extracted_rows": extracted_rows,
        "extracted_rows_review": review_rows,
        "fetch_log": fetch_log,
        "per_doc": per_doc,
        "n_screened": total,
        "n_passed": total,
        "n_downloaded": total,
        "n_extracted": n_ext,
        "needs_user_upload": [],
        "_dep_note": (None if pdf_extractor is not None
                      else "pdf_extractor 不可用（缺 fitz/pdfplumber）：PDF 已落盘，待人工补抽取"),
        "note": "已从上传的 PDF 直接抽取 2×2 表（A4 红线 · 须人工核验放行）",
    }


# ---------------------------------------------------------------------------
# A4 自动闭环辅助：A3 摘要门控 → 自动落盘 OA PDF → pdf_extractor 抽取 2×2 表
# ---------------------------------------------------------------------------
# ⚠️ 懒加载约束：pdf_extractor 依赖 fitz/pdfplumber（仅 anaconda 等含 PDF 依赖的
#    Python 有）。block_a 是共享模块，被 fullflow/run_case_human 在 managed Python 下
#    导入时不应因缺 PDF 库而整体 import 失败，故仅在此函数内局部 import。
def _pick_candidate(study):
    """返回 (kind, ident) 或 None。优先级：直链 PDF > pmid(PMC) > doi(Unpaywall) > doi(PMC-OA)。"""
    u = (study.get("url") or study.get("open_access_url") or "").strip()
    if u.lower().endswith(".pdf") or "europepmc" in u.lower() or u.rstrip("/").endswith("/pdf"):
        return ("url", u)
    if study.get("pmid"):
        return ("pmid", str(study["pmid"]))
    if study.get("doi"):
        return ("doi", str(study["doi"]))
    return None


def _resolve_pdf_url(cand, email):
    import pdf_fetch
    kind, ident = cand
    if kind == "url":
        return ident
    if kind == "pmid":
        return pdf_fetch.pmid_to_pdf(ident)
    if kind == "doi":
        return pdf_fetch.doi_to_pdf(ident, email) or pdf_fetch.doi_to_pmc_pdf(ident)
    return None


def _is_pdf(path):
    try:
        with open(path, "rb") as f:
            return f.read(5).startswith(b"%PDF")
    except Exception:  # noqa: BLE001
        return False


def _derive_inclusion_hints(topic):
    """从自由文本主题派生纳入门控词（去停用词）。ANY 命中即纳入（宽松 OR 语义）。

    仅作离线启发式兜底；用户可显式传 inclusion_hints 覆盖。派生为空时返回 None
    （A3 退化为「默认全纳入 + 记录摘要」）。
    """
    import re
    stop = {"the", "a", "an", "of", "for", "in", "on", "with", "and", "or", "vs",
            "versus", "to", "from", "patients", "patient", "study", "meta",
            "analysis", "randomized", "randomised", "trial", "effect", "outcome",
            "comparison", "group", "using", "type", "adult", "adults"}
    toks = re.findall(r"[a-z0-9][a-z0-9\-]{2,}", (topic or "").lower())
    hints = sorted({t for t in toks if t not in stop})
    return hints or None


# ── A4 PDF 统一缓存目录（绝对路径，不依赖启动 cwd；a4_stream / seam_test / 工作台上传
#    端点全部共享此目录，避免「adapters/pdfs 与 workbench/pdfs 双目录并存」「从不同 cwd
#    启动落到不同目录」「docN 覆盖式命名」导致的互相覆盖与重复下载）。
A4_PDF_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf_cache")


def _pdf_stem(study):
    """A4 PDF 落盘的稳定文件基名（同一文献跨轮次恒定）。

    优先用 DOI（文件名可读），无 DOI 时用标题 md5 前 10 位。稳定命名是
    「重跑不重复下载」的基础：同名文件存在且确为真 PDF 即直接复用。
    """
    import hashlib
    doi = str((study or {}).get("doi") or "").strip().lower()
    if doi:
        slug = re.sub(r"[^a-z0-9]+", "_", doi).strip("_")[:90]
        if slug:
            return "doi_" + slug
    title = str((study or {}).get("title") or "").strip().lower()
    return "t_" + (hashlib.md5(title.encode("utf-8")).hexdigest()[:10] if title else "notitle")


def _a4_cached_pdf(study, pdf_dir, cache_map=None):
    """查该文献已落盘的 PDF（跨轮次复用，避免重复下载）。

    三级查找：① cache_map（调用方由上一轮 A4 结果 per_doc 建立，可兼容旧的
    docN.pdf 命名）；② 当前稳定命名文件；③ 裸 DOI 命名（兼容旧版 /a4_stream
    未带协议前缀时落盘的 doi_<裸doi>.pdf）。命中且确为真 PDF 才复用。
    """
    key = str((study or {}).get("doi") or (study or {}).get("title") or "").strip().lower()
    if key and cache_map:
        p = cache_map.get(key)
        if p and os.path.isabs(p) and os.path.exists(p) and _is_pdf(p):
            return p
    p = os.path.join(pdf_dir, _pdf_stem(study) + ".pdf")
    if os.path.exists(p) and _is_pdf(p):
        return p
    # ③ 裸 DOI 兼容：旧版把 PDF 存为 doi_<去掉 https://doi.org/ 的裸 doi stem>
    doi = str((study or {}).get("doi") or "").strip().lower()
    if doi:
        bare = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi).strip("/")
        if bare:
            slug = re.sub(r"[^a-z0-9]+", "_", bare).strip("_")[:90]
            lp = os.path.join(pdf_dir, "doi_" + slug + ".pdf")
            if os.path.exists(lp) and _is_pdf(lp):
                return lp
    return None


def _a4_extract_pdf(pdf_path, pdf_extractor):
    """对已落盘 PDF 抽取 2x2 表。返回 (rows, tworows, n_candidates, err, candidates, doc_info)。

    n_candidates：真实可抽取信号数 = 结构化行(to_a4_rows) + 正文计数候选
    （事件/总数 提及，含 p 值）。之前只数 p 值候选，会误导"抽了但没用"。
    candidates：透传给工作台逐篇面板，展示"正文计数提及（需人工判断）"。
    doc_info：{type, confidence, excluded, signals, type_notice}。
    **excluded 恒为 False**（2026-09-10 规则变更）：人工在 A3 已确认文献类型，下层一律
    不再做类型判断，类型只作**标注/提示**（type_notice），绝不作为抽取门。
    （历史：v0.3–2026-09-09 曾由 extract() 内置规律 R1 强制甄别门把综述/指南判为
    excluded=True，消费点标 excluded_review——该机制已移除。）
    """
    # 功能开关（2026-09-17）：网页只提供「PDF 下载」时不抽取 —— 直接复用
    # 「pdf_extractor 不可用」这条既有降级路径：PDF 照常落盘，逐篇状态记为
    # 已下载/未抽取，extracted_rows 为空（故 Block B 无数据可算，流程到下载为止）。
    if not features.a4_extraction_enabled():
        return [], [], 0, None, [], None
    if pdf_extractor is None:
        return [], [], 0, None, [], None
    try:
        res = pdf_extractor.extract(pdf_path)
        rows = pdf_extractor.to_a4_rows(res) or []
        cands = res.get("candidates") or []
        n_cand = len(rows) + len(cands)
        _rs = res.get("review_summary") or {}
        doc_info = {"type": res.get("doc_type"),
                    "confidence": res.get("doc_type_confidence"),
                    # 键位保留以兼容旧消费点，但恒 False —— 类型不再构成排除依据。
                    "excluded": False,
                    "signals": _rs.get("signals") or [],
                    "type_notice": _rs.get("type_notice")}
    except Exception as e:  # noqa: BLE001
        return [], [], 0, f"{type(e).__name__}: {e}", [], None
    tworows = [r for r in rows if all(r.get(k) is not None for k in ("ai", "bi", "ci", "di"))]
    return rows, tworows, n_cand, None, cands, doc_info


def _a4_extract_section_texts(studies, pdf_dir, max_per_pdf=6000):
    """对已下载的 PDF 抽取章节文本，返回 {study_key: {title, doi, sections}}。

    用于下游 C 档写作参考。只处理已落盘（缓存命中）的 PDF，不重新下载。
    study_key 优先 doi、退其次 title（与 _a4_cached_pdf 同构）。
    """
    from pdf_extractor import extract_sections
    out = {}
    if not pdf_dir or not os.path.isdir(pdf_dir):
        return out
    for s in studies or []:
        cached = _a4_cached_pdf(s, pdf_dir)
        if not cached or not os.path.isfile(cached):
            continue
        secs = extract_sections(cached, max_chars_per_section=max_per_pdf)
        secs = {k: v for k, v in secs.items() if v and v.strip()}
        if secs:
            key = str(s.get("doi") or s.get("title") or "").strip().lower()
            if key:
                out[key] = {"title": s.get("title"), "doi": s.get("doi"), "sections": secs}
    return out


def _a4_fetch_one(cand, out_path, email, pdf_extractor, study=None):
    """单篇「解析直链 → 下载 → 抽取」（纯 IO/CPU、无共享状态 → 可并行）。

    **不做下载前类型甄别**（2026-09-10 起）：A3 裁决表即权威清单，A4 按清单逐篇下载，
    不再按类型剔除人工已纳入的综述/指南。类型仅在抽取后作为标注（见 a4_stream 的
    is_review / review_note），不再作为门。抽取层自身的类型甄别（pdf_extractor 的
    review_summary.excluded）不在本函数职责内。

    本地直链下载失败时，若 study 含 DOI，自动委托 coze publisher_pdf_batch
    （服务端真实浏览器 + 补充链）救援反爬/付费墙出版商 PDF，落盘到同一缓存目录
    后走统一抽取。coze 不可用时静默降级为 needs_upload（与旧行为一致）。

    返回 (out, events)：out 为该篇最终状态，events 为过程事件（downloading /
    extracting），由主循环按 index 顺序统一 emit。
    """
    import pdf_fetch
    evs = []
    # ── 直接下载：不做下载前类型甄别 ──
    # 设计变更（2026-09-10）：A3 已由人工在裁决表上定稿，「裁决表即权威清单」。
    # A4 只负责「下载 → 抽取」，不再按类型（综述/指南/方案）重新筛掉人工已纳入的篇目
    # —— 否则与人工裁决打架，且需要 _skip_page_screen 之类的豁免补丁来对齐。
    # 类型信息仍在抽取后以 is_review / review_note 形式**标注**（见 a4_stream），仅供人工参考。
    url = _resolve_pdf_url(cand, email)
    if not url:
        return ({"event": "failed", "status": "needs_upload", "gate": "pass_no_oa",
                 "reason": "通过门控但无 OA 副本（付费墙），需用户上传 PDF",
                 "pdf": None, "rows": [], "n_rows": 0, "n_tworows": 0}, evs)
    evs.append({"event": "downloading", "url": url})
    if not pdf_fetch.download(url, out_path) or not _is_pdf(out_path):
        # 本地直链下载失败 → 委托 coze 服务端真实浏览器救援（反爬/付费墙出版商）
        coze_ok = False
        doi = (study or {}).get("doi")
        if doi:
            evs.append({"event": "coze_rescue", "doi": doi})
            try:
                from pdf_fetch import _coze_pdf_download
                info = _coze_pdf_download(doi, out_path)
                coze_ok = bool(info) and _is_pdf(out_path)
            except Exception:
                coze_ok = False
        if not coze_ok:
            return ({"event": "failed", "status": "needs_upload", "gate": "pass_download_fail",
                     "reason": "通过门控但下载失败/非真 PDF，需用户上传 PDF",
                     "pdf": None, "rows": [], "n_rows": 0, "n_tworows": 0}, evs)
    if pdf_extractor is None:
        return ({"event": "downloaded_no_extract", "status": "downloaded_no_extract",
                 "gate": "pass_downloaded", "reason": "PDF 已下载，待补抽取",
                 "pdf": out_path, "rows": [], "n_rows": 0, "n_tworows": 0}, evs)
    evs.append({"event": "extracting", "pdf": out_path})
    # _a4_extract_pdf 自 v0.3 起返回 **6 元组**（末位 doc_info）。此处曾漏改，仍是 5 元组解包
    # → 每次下载成功都抛 ValueError，被 a4_stream 的 except 兜成 gate=worker_error /
    # status=needs_upload，表现为「首轮全篇补传、重跑（走缓存分支）却正常」。
    # 2026-09-10 修正为 6 元组，与 :1013 / :1420 两个调用点对齐。
    rows, tworows, n_cand, err, cands, doc_info = _a4_extract_pdf(out_path, pdf_extractor)
    if err:
        return ({"event": "failed", "status": "needs_upload", "gate": "extract_fail",
                 "reason": f"PDF 下载成功但抽取失败：{err}",
                 "pdf": out_path, "rows": [], "n_rows": 0, "n_tworows": 0}, evs)
    # 类型仅作标注（doc_type），不作为门——与「A3 裁决表即权威清单」一致。
    return ({"event": "extracted", "status": "extracted", "gate": "pass_downloaded",
             "reason": None, "pdf": out_path, "rows": rows, "candidates": cands,
             "n_rows": len(rows), "n_tworows": len(tworows), "n_candidates": n_cand,
             "doc_type": (doc_info or {}).get("type")}, evs)


def _ordered_parallel(items, workers, fn):
    """按提交顺序产出 fn 结果，内部以 workers 大小的滑动窗口并行执行。

    保证：① 并发度不超过 workers；② 输出顺序与 items 一致（前端按 index 定位
    行，乱序会让进度行跳动）。fn 须自行兜住异常，此处仅兜底跳过异常项。
    """
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=workers) as ex:
        it = iter(items)
        pending, nxt_seq, seq = {}, 0, 0
        for _ in range(workers):
            try:
                item = next(it)
            except StopIteration:
                break
            pending[nxt_seq] = ex.submit(fn, item)
            nxt_seq += 1
        while pending:
            fut = pending.pop(seq)
            try:
                res = fut.result()
            except Exception:  # noqa: BLE001 — fn 未兜住的异常不得拖垮整批
                res = None
            if res is not None:
                yield res
            try:
                item = next(it)
            except StopIteration:
                pass
            else:
                pending[nxt_seq] = ex.submit(fn, item)
                nxt_seq += 1
            seq += 1


def _read_doc_type(sc, study):
    """只读文献类型（A4 侧唯一的取值入口，**不做任何判定**）。

    权威值来自 A3 裁决表（人工确认优先，其次规则预填）；study 自带字段兜底。
    返回 (doc_type_or_None, source_or_None)。
    """
    sc = sc if isinstance(sc, dict) else {}
    s = study if isinstance(study, dict) else {}
    dt = sc.get("doc_type") or s.get("doc_type") or None
    src = sc.get("doc_type_source") or ("a3" if sc.get("doc_type") else None)
    return dt, src


def a4_stream(studies, screened, pdf_dir=None, max_attempts=12,
              inclusion_hints=None, email=None, workers=4, pdf_cache_map=None,
              cached_only=False):
    """生成器：逐篇研究执行 A4 下载+抽取，实时 yield 进度事件（供工作台实时预览）。

    每次 yield 一个事件 dict，关键字段：
      event: start | cached | skip | failed | deferred | downloading |
             extracting | extracted | downloaded_no_extract | done | error
      index / total / title / doi / gate / reason / url / pdf / n_rows / n_tworows
    失败不中断（继续处理下一篇）。末次 yield 为
      {"event": "done", "result": {<完整 a4_auto_fetch_and_extract dict>}}。

    workers：下载/抽取并发度（默认 4）。事件仍按 index 顺序产出，前端观感与串行
    一致，整体耗时近似降为 1/workers。
    pdf_cache_map：{文献 key(doi|title 小写) → 已落盘 PDF 绝对路径}；命中即跳过
    下载、直接抽取（emit cached），实现「重跑不重复下载」。
    同步封装 a4_auto_fetch_and_extract 与原行为一致（消费至 done 取 result）。
    """
    import pdf_fetch
    if email is None:
        email = pdf_fetch.DEFAULT_EMAIL
    if pdf_dir is None:
        pdf_dir = A4_PDF_CACHE_DIR
    os.makedirs(pdf_dir, exist_ok=True)

    # study→screened 按 doi/title 对齐（二者顺序一致亦可 zip）
    def _key(s):
        return str((s or {}).get("doi") or (s or {}).get("title") or "").strip().lower()
    scr_by_key = {_key(s): s for s in screened if isinstance(s, dict)}

    # pdf_extractor 懒加载（缺 PDF 库时优雅降级：仅落盘不抽取）
    try:
        import pdf_extractor  # noqa: F401
    except Exception as e:  # noqa: BLE001
        pdf_extractor = None
        _dep_note = f"pdf_extractor 不可用（缺 fitz/pdfplumber）：{type(e).__name__}: {e}"
    else:
        _dep_note = None

    studies_list = [s for s in studies if isinstance(s, dict)]
    total = len(studies_list)

    def _emit(ev):
        ev.setdefault("total", total)
        return ev

    extracted_rows = []        # 仅 2x2 结局表（ai/bi/ci/di 齐全）→ 供下游 B1 合并
    review_rows = []           # 全量抽取行（含连续量/描述性）→ 供 A4 人工核验
    fetch_log = []
    needs_upload = []
    per_doc = [None] * total   # 逐篇分组（按 index 定位，供工作台 A4 逐篇展示）
    n_passed = n_dl = n_ext = n_fetch = 0

    # ── 阶段 1：纯本地判定（零网络）。逐篇 yield start/skip/no_candidate/deferred，
    #    将「需下载」与「可复用缓存」的篇目按 index 顺序放入 work 队列。
    work = []
    for i, s in enumerate(studies_list):
        sc = scr_by_key.get(_key(s)) or {}
        title = s.get("title") or ""
        doi = s.get("doi")
        meta = {"index": i, "total": total, "title": title, "doi": doi}
        # 类型只读（A3 确认值）——占位分支（skip/needs_upload/deferred）同样带上，
        # 保证 A4 逐篇面板三处读到同一值，不出现"有的行有类型、有的没有"。
        _dt, _dt_src = _read_doc_type(sc, s)
        _dt_anno = {"doc_type": _dt, "doc_type_source": _dt_src,
                    "is_review": bool(_dt in DOC_TYPE_NO_PRIMARY)}

        # 门控以 decision_of() 为准（人工显式 decision 优先于 include 布尔）：
        # review-guard 默认排除的综述，人工在裁决下拉翻为「纳入」后此处即放行。
        if sc and decision_of(sc) == DECISION_EXCLUDE:
            r = {"title": title, "doi": doi, "gate": "relevance_skip",
                 "reason": sc.get("reason", "未通过摘要相关性门控")}
            fetch_log.append(r)
            per_doc[i] = {"index": i, "title": title, "doi": doi, "status": "skip",
                          "reason": r["reason"], "pdf": None, "rows": [],
                          "n_tworows": 0, **_dt_anno}
            # 仅抽本地已下载模式下，跳过的篇目不进实时抽取列表（与待上传篇目一致）；
            # 其状态仍记入 per_doc(status=skip)，供 A4 逐篇文档面板展示，且不进 needs_upload。
            if not cached_only:
                yield _emit({"event": "skip", **meta, **r})
            continue
        n_passed += 1

        cand = _pick_candidate(s)
        cached = _a4_cached_pdf(s, pdf_dir, pdf_cache_map)

        # 仅抽本地已下载：无 PDF 的篇目不排队、不进入实时抽取列表；
        # 仍记入 per_doc(status=needs_upload) 与 needs_upload，供 done 后「待上传」面板展示与补传。
        if cached_only and cached is None:
            r = {"title": title, "doi": doi, "gate": "no_local_pdf",
                 "reason": "本地无已下载 PDF，本次仅抽本地已下载篇目（待上传的请在下方列表补传后重跑）"}
            fetch_log.append(r); needs_upload.append(r)
            per_doc[i] = {"index": i, "title": title, "doi": doi, "status": "needs_upload",
                          "reason": r["reason"], "pdf": None, "rows": [],
                          "n_tworows": 0, **_dt_anno}
            continue  # 不 yield 任何事件 → 不出现在实时抽取列表

        yield _emit({"event": "start", **meta})

        if not cand:
            r = {"title": title, "doi": doi, "gate": "no_candidate",
                 "reason": "通过相关性门控但无下载入口（无 PMID/DOI/直链），需用户上传 PDF"}
            fetch_log.append(r); needs_upload.append(r)
            per_doc[i] = {"index": i, "title": title, "doi": doi, "status": "needs_upload",
                          "reason": r["reason"], "pdf": None, "rows": [],
                          "n_tworows": 0, **_dt_anno}
            yield _emit({"event": "failed", **meta, **r})
            continue

        if cached is None:
            # 配额按「实际发起下载数」计（缓存复用不消耗；付费墙/网络失败不消耗），
            # 确保可下载的 OA 论文不被饿死
            if n_fetch >= max_attempts:
                r = {"title": title, "doi": doi, "gate": "quota_deferred",
                     "reason": f"已达 max_attempts={max_attempts} 篇实际下载，其余通过门控者留待下一轮"}
                fetch_log.append(r)
                per_doc[i] = {"index": i, "title": title, "doi": doi, "status": "deferred",
                              "reason": r["reason"], "pdf": None, "rows": [],
                              "n_tworows": 0, **_dt_anno}
                yield _emit({"event": "deferred", **meta, **r})
                continue
            n_fetch += 1
            work.append((i, s, cand, os.path.join(pdf_dir, _pdf_stem(s) + ".pdf"), None))
        else:
            work.append((i, s, cand, cached, cached))

    # ── 阶段 2：下载 + 抽取（并发执行，按 index 顺序产出事件与结果）
    def _run(item):
        i, s, cand, out_path, cached = item
        title, doi = s.get("title") or "", s.get("doi")
        base = {"index": i, "total": total, "title": title, "doi": doi}
        try:
            if cached:
                evs = [{"event": "cached", "pdf": cached, **base}]
                if pdf_extractor is not None:
                    evs.append({"event": "extracting", "pdf": cached, **base})
                rows, tworows, n_cand, err, cands, doc_info = _a4_extract_pdf(cached, pdf_extractor)
                if pdf_extractor is None:
                    out = {"event": "downloaded_no_extract", "status": "downloaded_no_extract",
                           "gate": "pass_downloaded", "reason": "PDF 已下载，待补抽取",
                           "pdf": cached, "rows": [], "n_rows": 0, "n_tworows": 0}
                elif err:
                    out = {"event": "failed", "status": "needs_upload", "gate": "extract_fail",
                           "reason": f"PDF 已缓存但抽取失败：{err}",
                           "pdf": cached, "rows": [], "n_rows": 0, "n_tworows": 0}
                # 类型不再构成排除分支（2026-09-10 规则）：缓存分支与下载路径行为一致，
                # 同一篇 PDF 首轮/重跑结论相同。类型只经 doc_type 标注透出。
                else:
                    out = {"event": "extracted", "status": "extracted", "gate": "pass_downloaded",
                           "reason": None, "pdf": cached, "rows": rows, "candidates": cands,
                           "n_rows": len(rows), "n_tworows": len(tworows),
                           "n_candidates": n_cand, "cached": True,
                           "doc_type": (doc_info or {}).get("type")}
            else:
                out, evs = _a4_fetch_one(cand, out_path, email, pdf_extractor, study=s)
                evs = [{**e, **base} for e in evs]
        except Exception as e:  # noqa: BLE001 — 单篇异常不得拖垮整批
            out = {"event": "failed", "status": "needs_upload", "gate": "worker_error",
                   "reason": f"处理异常：{type(e).__name__}: {e}",
                   "pdf": None, "rows": [], "n_rows": 0, "n_tworows": 0}
            evs = []
        return i, out, evs

    nw = max(1, int(workers or 1))
    results = ((_run(it) for it in work) if nw == 1 else _ordered_parallel(work, nw, _run))
    for i, out, evs in results:
        s = studies_list[i]
        sc = scr_by_key.get(_key(s)) or {}
        title, doi = s.get("title") or "", s.get("doi")
        # 文献类型：**只读 A3 裁决表的权威值**（人工确认优先，其次规则预填）。
        # A4 不再自行判定类型；抽取层自己探测到的类型只作提示词（detected），
        # 与确认值不一致时显式提示，绝不改变裁决。
        dt_confirmed, dt_src = _read_doc_type(sc, s)
        dt_detected = out.get("doc_type") or None
        dt_effective = dt_confirmed or dt_detected
        is_review_eff = dt_effective in DOC_TYPE_NO_PRIMARY
        for e in evs:
            yield _emit(dict(e))
        pdf = out.get("pdf")
        rows = out.get("rows") or []
        n_tworows = out.get("n_tworows") or 0
        if out["status"] == "extracted":
            tworows = [r for r in rows if all(r.get(k) is not None for k in ("ai", "bi", "ci", "di"))]
            # 可计算效应量行（te/sete 齐全且来自表格模板，anchor 含 'table#'）：
            # 表格行 = 原文结构化报告（作者自算 HR/OR/RR 或 m±SD），可安全进 B 合并；
            # 叙述行（anchor 含 'text:'）多为综述正文对他引结果的转述，非本篇原始数据 → 不收。
            eff_rows = [dict(r, TE=r.get("te"), seTE=r.get("sete"))
                        for r in rows
                        if r.get("te") is not None and r.get("sete") is not None
                        and str(r.get("anchor") or "").startswith("p") and "table#" in str(r.get("anchor") or "")]
            n_dl += 1
            n_ext += len(tworows) + len(eff_rows)
            extracted_rows.extend(tworows)
            extracted_rows.extend(eff_rows)
            review_rows.extend(rows)
            fetch_log.append({"title": title, "doi": doi, "gate": "pass_downloaded",
                              "pdf": pdf, "n_rows": len(rows), "n_tworows": len(tworows),
                              "n_candidates": out.get("n_candidates", 0),
                              **({"cached": True} if out.get("cached") else {})})
        elif out["status"] == "downloaded_no_extract":
            n_dl += 1
            fetch_log.append({"title": title, "doi": doi, "gate": "pass_downloaded", "pdf": pdf,
                              "n_rows": 0, "n_tworows": 0, "n_candidates": 0,
                              "note": "PDF 已落盘，但缺 PDF 抽取库，待人工/环境补抽取"})
        else:
            # 无 excluded_review 分支（2026-09-10 起）：类型不再产生排除状态，
            # 走到这里的只有"下载/抽取失败 → 需补传"。
            r = {"title": title, "doi": doi, "gate": out.get("gate", "failed"),
                 "reason": out.get("reason"), **({"pdf": pdf} if pdf else {})}
            fetch_log.append(r); needs_upload.append(r)
        per_doc[i] = {"index": i, "title": title, "doi": doi, "status": out["status"],
                      "reason": out.get("reason"), "pdf": pdf, "rows": rows,
                      "candidates": out.get("candidates") or [],
                      "n_rows": len(rows), "n_tworows": n_tworows,
                      # doc_type = A3 裁决表确认值（权威，只读）；detected = 抽取层
                      # 自己的探测（提示词，仅在与确认值不一致时提示）
                      "doc_type": dt_effective,
                      "doc_type_confirmed": dt_confirmed,
                      "doc_type_source": dt_src or ("detected" if dt_detected else None),
                      "doc_type_detected": dt_detected,
                      # 类型仅作标注（提示位）：不参与任何排除判定
                      "is_review": is_review_eff,
                      # 是否真正纳入由 A3 裁决表决定，A4 不再据此排除
                      "included": True,
                      **({"cached": True} if out.get("cached") else {})}
        # 抽取层与 A3 确认值不一致 → 提示词（不改裁决，不回写类型）
        if dt_confirmed and dt_detected and dt_detected != dt_confirmed:
            per_doc[i]["doc_type_notice"] = (
                "ℹ 抽取层探测为「%s」，与 A3 确认的「%s」不一致——以 A3 确认为准；"
                "如需改判请回到 ③ 初筛（裁决表类型列）" %
                (DOC_TYPE_LABELS.get(dt_detected, dt_detected),
                 DOC_TYPE_LABELS.get(dt_confirmed, dt_confirmed)))
        # 类型为无原始数据的类别却抽出 0 行 → 提示属正常，避免误判"抽取失败"
        if is_review_eff and out["status"] == "extracted" and len(rows) == 0:
            per_doc[i]["review_note"] = ("⚠ A3 确认的文献类型为「%s」，本类文献通常无原始 2×2 表，"
                "抽取为 0 行属正常；如需原始数据请打回到 ③ 初筛重新确认类型或裁决"
                % DOC_TYPE_LABELS.get(dt_effective, dt_effective))
        yield _emit({"event": out["event"], "index": i, "total": total, "title": title,
                     "doi": doi, "gate": out.get("gate"), "reason": out.get("reason"),
                     "pdf": pdf, "n_rows": len(rows), "n_tworows": n_tworows,
                     **({"cached": True} if out.get("cached") else {})})

    result = {
        "extracted_rows": extracted_rows,
        "extracted_rows_review": review_rows,
        "fetch_log": fetch_log,
        "per_doc": per_doc,
        "n_screened": total,
        "n_passed": n_passed,
        "n_downloaded": n_dl,
        "n_extracted": n_ext,
        "needs_user_upload": needs_upload,
        # 下载结果统计（2026-09-17）：A4 降级为「PDF 下载」后，「下载概览」直接读这两个
        # 计数，不必前端再遍历 per_doc。failed = 抓取失败、需人工处理；needs_upload = 需补传。
        "n_failed": sum(1 for d in per_doc if d.get("status") == "failed"),
        "n_needs_upload": len(needs_upload),
        "_dep_note": _dep_note,
    }
    yield _emit({"event": "done", "result": result})


def a4_auto_fetch_and_extract(studies, screened, pdf_dir=None, max_attempts=12,
                              inclusion_hints=None, email=None, on_a4_event=None,
                              workers=4, pdf_cache_map=None):
    """A3 摘要门控 → 自动落盘 OA 全文 PDF → pdf_extractor 抽取 2×2 表（同步封装）。

    消费 a4_stream 至 done，返回完整结果 dict（与原实现行为一致）。
    on_a4_event：可选回调 f(ev)，实时转发 a4_stream 的逐篇进度事件
    （start/cached/downloading/extracting/extracted/failed/...），供工作台续跑路径实时上屏。
    workers / pdf_cache_map：透传给 a4_stream（并发度 / 已落盘 PDF 复用映射）。
    """
    last = None
    for ev in a4_stream(studies, screened, pdf_dir=pdf_dir, max_attempts=max_attempts,
                        inclusion_hints=inclusion_hints, email=email, workers=workers,
                        pdf_cache_map=pdf_cache_map):
        if on_a4_event:
            try:
                on_a4_event(ev)
            except Exception:  # noqa: BLE001 — 回调异常不得拖垮抽取
                pass
        if ev.get("event") == "done":
            last = ev["result"]
    return last


def a4_persist_result(session_path, result):
    """把 A4 预览结果（含 per_doc 逐篇分组、pdf 绝对路径、页码锚点）落盘到会话。

    供工作台「逐篇文档展示」直接读取（STATE.await.a4_result），并支持上传 PDF 后
    就地回写单篇状态。同时兼容 legacy data[\"await\"]。

    注意：必须用引用链（setdefault 原地修改），不要写 ``x = (d or {}).setdefault(...)``
    这类会把空字典替换成字面量、从而断开与 sess.data 引用的写法。
    """
    from fullflow import FullflowSession
    sess = FullflowSession.load(session_path)
    lv = sess.data.get("last_view")
    if not isinstance(lv, dict):
        lv = {}
        sess.data["last_view"] = lv
    ff = lv.setdefault("fullflow", {})
    aw = ff.setdefault("await", {})
    aw["a4_result"] = result
    legacy = sess.data.get("await")
    if isinstance(legacy, dict):
        legacy["a4_result"] = result
        sess.data["await"] = legacy
    sess.save()
    return result


def a4_get_result(session_path):
    """读取已落盘的 A4 结果（无则返回 None）。"""
    from fullflow import FullflowSession
    sess = FullflowSession.load(session_path)
    ff = (sess.data.get("last_view") or {}).get("fullflow") or {}
    return (ff.get("await") or {}).get("a4_result")


# ===========================================================================
# A4「批量上传真实 PDF → 按 PDF 内部文章全名自动匹配到文章列表」
# （2026-09-09 重做：原实现是「粘贴 DOI/PMID/标题 文本清单做元数据比对」，
#   与用户预期不符；改为上传已下载的 PDF 文件、读 PDF 内标题/DOI、模糊匹配列表文章）
# ===========================================================================
def _clean_title(t):
    if not t:
        return ""
    t = re.sub(r"\s+", " ", str(t)).strip()
    return t.strip(" .;:-\t")[:300]


def _norm_title(t):
    """标题归一化（去标点/小写/合空格），仅保留字母数字与中文，供模糊比对。"""
    if not t:
        return ""
    t = str(t).lower()
    t = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def _norm_doi(d):
    """抽取并归一化 DOI（忽略 https://doi.org/ 前缀）。"""
    if not d:
        return ""
    d = str(d).strip().lower()
    m = re.search(r"10\.\d{4,9}/[-._;()/:a-z0-9]+", d)
    if m:
        return m.group(0).rstrip(".;)")
    return d


def _title_score(a, b):
    """标题相似度：0.5×序列比 + 0.5×token F 值（对长短差异更鲁棒）。"""
    import difflib
    na, nb = _norm_title(a), _norm_title(b)
    if not na or not nb:
        return 0.0
    seq = difflib.SequenceMatcher(None, na, nb).ratio()
    A, B = set(na.split()), set(nb.split())
    inter = len(A & B)
    if not inter:
        return seq * 0.5
    prec = inter / len(A)
    rec = inter / len(B)
    f = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    return 0.5 * seq + 0.5 * f


def _extract_pdf_title(path, max_pages=2):
    """从 PDF 内抽取文章标题：优先元数据 /Title，否则首页上半页最大字号文本块。"""
    try:
        import fitz
    except Exception:
        return ""
    try:
        doc = fitz.open(path)
    except Exception:
        return ""
    try:
        meta = (doc.metadata or {}).get("title") or ""
        if meta and len(meta.strip()) > 8:
            return _clean_title(meta)
        best = ""
        for pi in range(min(max_pages, doc.page_count)):
            page = doc[pi]
            try:
                d = page.get_text("dict")
            except Exception:
                d = None
            if not d:
                continue
            H = page.rect.height or 800
            spans = []
            for blk in d.get("blocks", []):
                if blk.get("type") != 0:
                    continue
                for line in blk.get("lines", []):
                    for span in line.get("spans", []):
                        txt = (span.get("text") or "").strip()
                        if not txt or len(txt) < 4:
                            continue
                        y0 = span.get("bbox", [0, 0, 0, 0])[1]
                        if y0 > H * 0.55:   # 只取上半页（标题通常在顶部）
                            continue
                        spans.append((span.get("size", 0), txt))
            if not spans:
                continue
            spans.sort(key=lambda x: -x[0])
            # 合并最大字号附近、连续相似字号的 span 作为标题（1～3 行）
            title_lines, cur_size = [], None
            for size, txt in spans:
                if cur_size is None or abs(size - cur_size) < 2.0:
                    if title_lines and abs(size - cur_size) < 2.0:
                        title_lines[-1] = title_lines[-1] + " " + txt
                    else:
                        title_lines.append(txt)
                    cur_size = size
                else:
                    break
                if len(title_lines) >= 3:
                    break
            cand = " ".join(title_lines).strip()
            # 排除明显的作者/机构行
            if re.search(r"et al|@|\buniversity\b|\bdepartment\b|\bhospital\b|\binstitute\b", cand, re.I):
                cand = ""
            if len(cand) > len(best):
                best = cand
        if best:
            return _clean_title(best)
        # 兜底：首页纯文本首行
        try:
            txt = doc[0].get_text("text") or ""
            lines = [l.strip() for l in txt.splitlines() if l.strip()]
            if lines:
                return _clean_title(lines[0][:200])
        except Exception:
            pass
        return ""
    finally:
        try:
            doc.close()
        except Exception:
            pass


def _extract_pdf_doi(path, max_pages=2):
    """从 PDF 首页文本抽取 DOI（强匹配信号）。"""
    try:
        import fitz
    except Exception:
        return ""
    try:
        doc = fitz.open(path)
    except Exception:
        return ""
    try:
        for pi in range(min(max_pages, doc.page_count)):
            txt = doc[pi].get_text("text") or ""
            m = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", txt)
            if m:
                return m.group(0).rstrip(".;)")
    finally:
        try:
            doc.close()
        except Exception:
            pass
    return ""


def _build_match_candidates(sess):
    """汇总「文章列表」候选：A2 检索结果 + A3 初筛 + 已有 per_doc，按归一标题去重。"""
    cands = []
    def add(title, doi=None, pmid=None, year=None, source=None, journal=None, origin=""):
        t = (title or "").strip()
        if not t:
            return
        cands.append({"title": t, "doi": doi, "pmid": pmid, "year": year,
                      "source": source, "journal": journal, "origin": origin})
    A = (sess.data.get("blocks", {}).get("A", {}).get("envelope") or {})
    for st in A.get("stages", []):
        sid = (st.get("stage") or {}).get("id")
        sr = st.get("stage_result") or {}
        if sid == "A2.literature_search":
            for s in (sr.get("studies") or []):
                add(s.get("title"), s.get("doi"), s.get("pmid"), s.get("year"),
                    s.get("source"), None, "A2")
        elif sid == "A3.screening":
            for s in (sr.get("screened") or []):
                add(s.get("title"), s.get("doi"), s.get("pmid"), s.get("year"),
                    s.get("source"), None, "A3")
    res = a4_get_result(sess.path) if getattr(sess, "path", None) else None
    if res:
        for d in (res.get("per_doc") or []):
            add(d.get("title"), d.get("doi"), d.get("pmid"), d.get("year"),
                None, d.get("journal"), "per_doc")
    seen, uniq = set(), []
    for c in cands:
        k = _norm_title(c["title"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(c)
    return uniq


def _match_candidates(title, doi, candidates, weak=0.4, strong=0.6):
    """把单个 PDF（title/doi）匹配到候选文章列表，返回 (best_idx, score, top3)。"""
    # DOI 强匹配（归一后相等即 100%）
    nd = _norm_doi(doi)
    if nd:
        for idx, c in enumerate(candidates):
            if _norm_doi(c.get("doi")) == nd:
                return idx, 1.0, [{"index": idx, "title": c.get("title"), "score": 1.0}]
    scored = [(idx, _title_score(title, c.get("title") or ""))
              for idx, c in enumerate(candidates)]
    scored.sort(key=lambda x: -x[1])
    top = [{"index": i, "title": candidates[i].get("title"), "score": round(s, 3)}
           for i, s in scored[:3]]
    if not scored or scored[0][1] < weak:
        return None, (scored[0][1] if scored else None), top
    return scored[0][0], scored[0][1], top


def a4_match_pdfs(session_path, pdf_paths, a4_cache_dir=None):
    """上传多份已下载 PDF → 抽标题/DOI → 模糊匹配文章列表 → 返回映射结构。
    上传的 PDF 直接落盘到 A4 缓存目录（up_<i>_<名>.pdf），供随后关联抽取复用。
    """
    from fullflow import FullflowSession
    if a4_cache_dir is None:
        a4_cache_dir = A4_PDF_CACHE_DIR
    os.makedirs(a4_cache_dir, exist_ok=True)
    sess = FullflowSession.load(session_path)
    candidates = _build_match_candidates(sess)
    matches = []
    for i, src in enumerate(pdf_paths):
        src = str(src)
        base = os.path.splitext(os.path.basename(src))[0] or ("pdf%d" % (i + 1))
        stem = "up_%d_%s" % (i + 1, re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", base)[:50].strip("_") or ("pdf%d" % (i + 1)))
        dst = os.path.join(a4_cache_dir, stem + ".pdf")
        try:
            shutil.copyfile(src, dst)
        except Exception:
            dst = src
        title = _extract_pdf_title(dst)
        doi = _extract_pdf_doi(dst)
        best_idx, score, top = _match_candidates(title, doi, candidates)
        matches.append({
            "pdf_name": os.path.basename(src),
            "pdf_path": dst,
            "pdf_title": title,
            "pdf_doi": doi,
            "matched_index": best_idx,
            "score": round(score, 3) if score is not None else None,
            "candidates": top,
        })
    return {"matches": matches, "candidates": candidates,
            "n_candidates": len(candidates)}


def a4_link_matches(session_path, mappings):
    """按前端确认的映射，把 PDF 关联到对应文章（写入 per_doc）。
    mappings: [{pdf_path, pdf_title, matched_index(int|null)}]；
    matched_index 非 null → 关联到候选文章（已存在则补 pdf 路径，否则新建 per_doc 条目）；
    为 null → 作为未匹配/新建篇目（needs_upload）保留，等待人工处理。
    """
    from fullflow import FullflowSession
    sess = FullflowSession.load(session_path)
    candidates = _build_match_candidates(sess)
    res = a4_get_result(session_path) or {}
    pds = res.get("per_doc") or []
    by_title, by_doi = {}, {}
    for d in pds:
        t = _norm_title(d.get("title") or "")
        if t:
            by_title[t] = d
        dd = _norm_doi(d.get("doi"))
        if dd:
            by_doi[dd] = d
    linked = 0
    for m in (mappings or []):
        pdf_path = m.get("pdf_path") or m.get("pdf_name") or ""
        title = (m.get("pdf_title") or "").strip()
        if not pdf_path or not os.path.exists(pdf_path):
            continue
        idx = m.get("matched_index")
        if isinstance(idx, int) and 0 <= idx < len(candidates):
            cand = candidates[idx]
            key_t = _norm_title(cand.get("title") or "")
            key_d = _norm_doi(cand.get("doi"))
            target = by_title.get(key_t) or (by_doi.get(key_d) if key_d else None)
            if target is None:
                target = {"index": len(pds), "title": cand.get("title"),
                          "doi": cand.get("doi"), "pmid": cand.get("pmid"),
                          "year": cand.get("year"), "journal": cand.get("journal"),
                          "status": "uploaded", "rows": [], "n_rows": 0,
                          "n_tworows": 0, "included": True, "is_review": False}
                pds.append(target)
                if key_t:
                    by_title[key_t] = target
                if key_d:
                    by_doi[key_d] = target
            target["pdf"] = pdf_path
            target["status"] = "uploaded"
            if not target.get("title"):
                target["title"] = title
            linked += 1
        else:
            target = {"index": len(pds), "title": title, "doi": None,
                      "status": "needs_upload", "rows": [], "n_rows": 0,
                      "n_tworows": 0, "included": True, "is_review": False,
                      "pdf": pdf_path}
            pds.append(target)
            linked += 1
    res["per_doc"] = pds
    a4_persist_result(session_path, res)
    return {"linked": linked, "n_per_doc": len(pds)}



#: 演示用原始数据（2026-09-17 用户要求）：用户在工作台首页选「我已备好原始数据 → 直接进 B」
#: 却**未提供任何数据**时，按此示例继续流程，作为合并计算的演示。
#: **按效应量分套** —— 二分类给 2×2 四格、连续给 mean/sd/n 两组、生存给 HR+CI，
#: 与首页「合并效应量尺度」下拉联动（见 workbench.html 的 DEMO_BY_EM，两处需同步改）。
DEMO_RAW_CSV_BY_EM = {
    "OR": "study,ai,bi,ci,di\nStudy A,30,70,15,85\nStudy B,22,78,18,82\n",
    "RR": "study,ai,bi,ci,di\nStudy A,30,70,15,85\nStudy B,22,78,18,82\n",
    "MD": ("study,mean_exp,sd_exp,n_exp,mean_ctrl,sd_ctrl,n_ctrl\n"
           "Study A,12.4,3.1,50,15.2,3.6,48\n"
           "Study B,9.8,2.7,42,11.5,3.0,45\n"),
    "SMD": ("study,mean_exp,sd_exp,n_exp,mean_ctrl,sd_ctrl,n_ctrl\n"
            "Study A,24.5,6.2,60,20.1,5.9,58\n"
            "Study B,18.7,5.4,45,21.3,5.7,47\n"),
    "HR": ("study,hr,ci_low,ci_high\n"
           "Study A,0.72,0.58,0.89\n"
           "Study B,0.81,0.66,0.99\n"),
}
DEMO_RAW_CSV = DEMO_RAW_CSV_BY_EM["OR"]   # 向后兼容（旧引用/默认 OR）


def demo_raw_csv(effect_measure="OR"):
    """按效应量取演示 CSV 文本（未知效应量回退 OR）。"""
    return DEMO_RAW_CSV_BY_EM.get(str(effect_measure or "OR").upper()) or DEMO_RAW_CSV


def demo_raw_rows(effect_measure="OR"):
    """解析对应效应量的内置演示数据为 extracted_rows。解析失败返回 []。"""
    try:
        return parse_raw_csv("demo.csv", text=demo_raw_csv(effect_measure)) or []
    except Exception:  # noqa: BLE001 — 演示数据异常不得抛出，由调用方决定兜底
        return []


def a3_pdf_download(studies, screened_studies, pdf_dir=None, max_attempts=12,
                    inclusion_hints=None, pdf_email=None, on_a4_event=None,
                    workers=4, pdf_cache_map=None):
    """A3 — PDF 全文下载（独立阶段；2026-09-17 用户裁定从 A4 拆出）。

    只按 A2 裁决清单逐篇下载开放获取（OA）全文，**不做任何数据抽取**。
    实现上直接复用 `a4_auto_fetch_and_extract`：features.a4_extraction 关闭时其抽取路径
    已在 `_a4_extract_pdf` 短路，因此同一实现天然「只下载」（extracted_rows 恒为空）。
    A4（数据提取）启用时再由 A4 阶段对已落盘 PDF 抽取（pdf_cache_map 命中 → 不重复下载）。

    返回 (stage_result, nha)；stage_result 与 a4_auto_fetch_and_extract 同构，便于前端复用。
    """
    nha = {
        "type": "confirm",
        "prompt": ("PDF 全文下载完成。核对下方逐篇下载清单（PDF 路径可点开预览）；"
                   "如需继续做合并分析，可在本节点上传你整理好的数据直接跳到 B 部分。"),
        "required": True,
        "gate": "none",
        "options": ["approved", "rejected"],
    }
    try:
        af = a4_auto_fetch_and_extract(
            studies, screened_studies, pdf_dir=pdf_dir,
            max_attempts=max_attempts, inclusion_hints=inclusion_hints,
            email=pdf_email, on_a4_event=on_a4_event,
            workers=workers, pdf_cache_map=pdf_cache_map,
        )
    except Exception as e:  # noqa: BLE001 — 下载整段失败不得拖垮 Block A
        result = {
            "extracted_rows": [], "per_doc": [], "fetch_log": [],
            "n_screened": len(screened_studies or []), "n_passed": 0,
            "n_downloaded": 0, "n_extracted": 0,
            "needs_user_upload": [], "n_failed": 0, "n_needs_upload": 0,
            "coze_ready": False,
            "note": f"A3 自动下载异常，降级为空结果：{type(e).__name__}: {e}",
        }
        return result, nha
    result = dict(af)
    result["note"] = ("PDF 全文下载完成（本节点不提供数据提取；"
                      "如需数据提取请开启 features.a4_extraction）")
    return result, nha


def _a3_result_of(sess):
    """取本会话 A3（PDF 下载）阶段结果（含 per_doc）。

    兼容两种落点：① Block A 信封里 A3 阶段（新）；② `last_view.await` 的
    `a4_result`（旧会话该节点曾是 A4，下载结果挂在那里）。取不到则返回 {}。
    """
    env = ((sess.data.get("blocks") or {}).get("A") or {}).get("envelope") or {}
    for st in (env.get("stages") or []):
        sid = (st.get("stage") or {}).get("id")
        if sid in (A3, A4):
            sr = st.get("stage_result") or {}
            if sr.get("per_doc"):
                return sr
    lv = ((sess.data.get("last_view") or {}).get("fullflow") or {}).get("await") or {}
    for key in ("a4_result", "stage_result"):
        sr = lv.get(key) or {}
        if sr.get("per_doc"):
            return sr
    return {}


def _downloadable_docs(result):
    """从 A3 结果筛出「可交付」篇目：已下载（有真实 PDF 文件）的排在前面。

    返回 [(doc, pdf_path_or_None)]；跳过 status == "skip"（筛选阶段已排除）。
    """
    out = []
    for d in (result.get("per_doc") or []):
        if not isinstance(d, dict) or d.get("status") == "skip":
            continue
        p = d.get("pdf")
        if p and not os.path.isfile(p):
            p = None          # 记录里写了路径但文件已不在（被清理）→ 按未获取处理
        out.append((d, p))
    out.sort(key=lambda t: (t[1] is None, t[0].get("index") or 0))
    return out


def _safe_filename(name, maxlen=60):
    """清洗为可用作文件名的字符串（去路径分隔与非法字符，限长）。"""
    s = re.sub(r'[\\/:*?"<>|\r\n\t]+', "_", str(name or "")).strip(" ._")
    return (s[:maxlen] or "document")


def _file_uri(path):
    """本地绝对路径 → Excel 可点的 file:/// URI（中文 / 空格按 URL 百分号编码）。

    用途：A3 确认清单里「PDF 文件」列做成超链接，用户下完清单直接点文件名即可打开本地 PDF。
    """
    from urllib.parse import quote
    drive, rest = os.path.splitdrive(os.path.abspath(str(path)))
    p = drive.replace("\\", "/") + rest.replace("\\", "/")   # C:\a\b → C:/a/b
    # safe="/:" —— 盘符冒号必须保留字面量，编码成 %3A 后 Excel 打不开；
    # 中文 / 空格仍需百分号编码。
    return "file:///" + quote(p, safe="/:")


def export_a3_download_list_xlsx(session_path, out_path):
    """导出 A3「PDF 全文下载」确认清单为 xlsx（人工可读、可归档）。

    列：序号 / 标题 / DOI / 年 / 刊名 / 状态 / PDF 文件名 / 说明（失败原因等）。
    依赖 openpyxl；缺失时抛出明确错误（由调用方转成 400 提示）。
    返回 (out_path, n_docs, n_downloaded)。
    """
    from fullflow import FullflowSession
    sess = FullflowSession.load(session_path)
    res = _a3_result_of(sess)
    docs = _downloadable_docs(res)
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"缺少 openpyxl，无法生成 xlsx：{e}")

    STATUS_ZH = {
        "extracted": "已下载", "downloaded_no_extract": "已下载",
        "uploaded": "已下载", "needs_upload": "未获取到",
        "failed": "下载失败", "downloading": "下载中",
        "start": "排队中", "deferred": "延后",
    }
    wb = Workbook()
    ws = wb.active
    ws.title = "PDF 下载清单"
    head = ["#（篇目序号）", "标题", "DOI", "年", "刊名", "状态", "PDF 文件", "说明"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
    n_dl = 0
    for d, pdf in docs:
        st = STATUS_ZH.get(d.get("status"), d.get("status") or "—")
        if pdf:
            n_dl += 1
        ws.append([
            (d.get("index") or 0) + 1,
            d.get("title") or "",
            d.get("doi") or "",
            d.get("year") or d.get("publication_date") or "",
            d.get("journal") or "",
            st,
            os.path.basename(pdf) if pdf else "",
            (d.get("reason") or d.get("review_note") or "") if not pdf else "",
        ])
        # 清单内的「PDF 文件」与「DOI」做成**可点链接**（2026-09-20 用户要求：
        # 清单需要能直接操作，文件名即入口）——PDF 指向本地绝对路径，DOI 指向 doi.org。
        _row = ws.max_row
        if pdf:
            ws.cell(row=_row, column=7).hyperlink = _file_uri(pdf)
        _doi = str(d.get("doi") or "").strip()
        if _doi:
            # 有的来源存的是完整 URL（https://doi.org/10.xxxx）→ 先剥前缀，避免
            # 拼成 https://doi.org/https://doi.org/10.xxxx（实测踩到，2026-09-20）。
            _bare = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", _doi, flags=re.I)
            ws.cell(row=_row, column=3).hyperlink = "https://doi.org/" + _bare
    for col, w in zip("ABCDEFGH", (5, 60, 28, 8, 26, 10, 30, 34)):
        ws.column_dimensions[col].width = w
    _hlink = Font(color="0563C1", underline="single")
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=(c.column_letter in ("B", "H")))
            if c.hyperlink is not None:
                c.font = _hlink          # 蓝字下划线，一眼看出可点
    ws.freeze_panes = "A2"
    wb.save(out_path)
    return out_path, len(docs), n_dl


def a3_pdf_zip(session_path, out_path):
    """把 A3 已下载的 PDF 打包为 zip（便于一次性取走全文）。

    归档名 = `NN_标题.pdf`（NN 为篇目序号，标题清洗限长），同名自动加序号避免覆盖。
    返回 (out_path, n_files)；无任何可打包 PDF 时抛出 ValueError。
    """
    import zipfile
    from fullflow import FullflowSession
    sess = FullflowSession.load(session_path)
    res = _a3_result_of(sess)
    docs = _downloadable_docs(res)
    used, n = set(), 0
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        for d, pdf in docs:
            if not pdf:
                continue
            base = "%02d_%s" % ((d.get("index") or 0) + 1,
                                _safe_filename(d.get("title") or "document", 70))
            arc, k = base + ".pdf", 1
            while arc.lower() in used:
                k += 1
                arc = "%s(%d).pdf" % (base, k)
            used.add(arc.lower())
            z.write(pdf, arcname=arc)
            n += 1
        # 附一份清单，便于对照（即使 Excel 没下也能看）
        try:
            import csv
            import io as _io
            buf = _io.StringIO()
            w = csv.writer(buf)
            w.writerow(["#", "title", "doi", "status", "pdf_file", "note"])
            for d, pdf in docs:
                w.writerow([(d.get("index") or 0) + 1, d.get("title") or "", d.get("doi") or "",
                            d.get("status") or "", os.path.basename(pdf) if pdf else "",
                            (d.get("reason") or "") if not pdf else ""])
            z.writestr("下载清单.csv", "\ufeff" + buf.getvalue())   # BOM：Excel 直开不乱码
        except Exception:  # noqa: BLE001
            pass
    if not n:
        raise ValueError("本会话没有已下载成功的 PDF 可打包（可能全部未获取到或文件已被清理）")
    return out_path, n


def a4_data_extraction(screened_studies, extraction_table=None, studies=None,
                       auto_fetch=False, auto_fetch_dir=None, max_attempts=12,
                       inclusion_hints=None, pdf_email=None, on_a4_event=None,
                       workers=4, pdf_cache_map=None):
    # 🔴 红线闸：效应量/事件数等关键字段须人工核验放行方可进 Block B
    nha = {
        "type": "approve",
        "prompt": "请人工核验提取数据（TE/seTE/事件数等关键字段），批准后方可进入 Block B 计算。",
        "required": True,
        "gate": "extraction_review",
    }

    # 路径 A：用户提供提取表（演示/数据路径）→ 解析即用，绝不联网
    if extraction_table is not None:
        rows = _parse_extraction(extraction_table)
        result = {
            "extracted_rows": rows,
            "n_screened": len(screened_studies),
            "n_extracted": len(rows) if isinstance(rows, list) else 0,
            "coze_ready": False,
            "note": "提取表由用户提供（手动/演示数据），待本闸人工核验。",
        }
        return result, nha

    # 路径 B：无提取表 + 有文献 + 开启 auto_fetch → A3 门控 → 自动落盘+抽取（草稿）
    if auto_fetch and studies:
        try:
            af = a4_auto_fetch_and_extract(
                studies, screened_studies, pdf_dir=auto_fetch_dir,
                max_attempts=max_attempts, inclusion_hints=inclusion_hints,
                email=pdf_email, on_a4_event=on_a4_event,
                workers=workers, pdf_cache_map=pdf_cache_map,
            )
        except Exception as e:  # noqa: BLE001
            # 自动抓取整段失败不得拖垮 Block A；降级回离线占位并如实说明
            result = {
                "extracted_rows": [],
                "n_screened": len(screened_studies),
                "n_extracted": 0,
                "coze_ready": False,
                "note": f"A4 自动抓取异常，降级为离线占位：{type(e).__name__}: {e}",
            }
            return result, nha

        dep = af.get("_dep_note")
        result = {
            "extracted_rows": af["extracted_rows"],
            "extracted_rows_review": af["extracted_rows_review"],
            "n_screened": af["n_screened"],
            "n_passed": af["n_passed"],
            "n_downloaded": af["n_downloaded"],
            "n_extracted": af["n_extracted"],
            "needs_user_upload": af["needs_user_upload"],
            "fetch_log": af["fetch_log"],
            "coze_ready": False,
            "note": ("已由 A3 摘要门控自动下载 OA 全文并抽取 2×2 表（草稿），须经本闸人工核验放行；"
                     "付费墙/无 OA 篇目已记录待用户上传 PDF。"
                     + (f" ⚠️ {dep}" if dep else "")),
        }
        return result, nha

    # 路径 C：无提取表也未开启 auto_fetch → 离线占位（旧行为，保持兼容）
    rows = []
    result = {
        "extracted_rows": rows,
        "n_screened": len(screened_studies),
        "n_extracted": 0,
        "coze_ready": False,
        "note": "提取草稿为离线占位；coze 部署后由 AI 生成提取表并经本闸人工核验。",
    }
    return result, nha


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


def _soft_stop(env, pid, stages, tool_card_outputs, stage, sid, pause_at, decisions):
    """P3 软停靠（fullflow HITL，spec contracts/fullflow/v0.1.0）。

    pause_at 含 sid 且未持对应 approved 凭据 → 提前软停返回
    （done=False / await_human=True / gate=None / pause=True，区别于红线闸）。
    """
    if not (pause_at and sid in pause_at) or _any_approve(decisions, sid):
        return None
    return {"pipeline_id": pid, "pipeline": env["pipeline"], "stages": stages,
            "attachments": [], "tool_card_outputs": tool_card_outputs or [],
            "done": False, "await_human": True, "gate": None, "final": stage,
            "pause": True, "human_decisions": []}


# ---------------------------------------------------------------------------
# 编排：A1 → A2（检索+初筛合并节点「文献集」）→ A4（本地优先；use_coze 占位待 coze 部署后启用）
# ---------------------------------------------------------------------------
def _picos_report_to_query(text):
    """A1 人工编辑版 PICOS 报告 → A2 检索主题串（用户需求 2026-09-19）。

    提取 P/I/C/O/S 表格行中可检索的值（跳过「待填」「疑似含对照」等占位），
    并附加表格外非空说明行（用户补充的自由文字）。抽不到任何值 → 整段原文。
    只做文本拼接，不做翻译 —— 后续统一走 _translate_topic_authoritative。

    清理规则（2026-09-19 二次需求）：说明行去掉「补充：/注：/备注：/说明：」等
    前缀标签与结尾标点（。；;，,），自由行内去掉**加粗/链接等 markdown 修饰**，
    保证「原始主题（输入）」面板只显示真正参与检索的内容。
    """
    if not isinstance(text, str) or not text.strip():
        return None
    vals, free_lines = [], []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        m = re.match(r"\|\s*([PIOSC])\s*\|\s*([^|\n]+?)\s*\|?\s*$", s)
        if m:
            v = m.group(2).strip()
            if v and "待填" not in v and "疑似" not in v and "待确认" not in v:
                vals.append(v)
        elif not s.startswith(("|", "#", "---", "—")):
            free_lines.append(s)

    def _clean(seg):
        # 去说明性前缀（补充：/注：/备注：/说明：/另外：等元标签；不动「随访：」这类有语义前缀）
        seg = re.sub(r"^(?:补充说明|补充|备注|说明|注意|另外|其他|重复|注|note)\s*[:：]\s*",
                     "", seg, flags=re.I)
        # 去 markdown 修饰（**加粗**、*斜体*、[文本](链接)→文本、`代码`）
        seg = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", seg)
        seg = seg.replace("**", "").replace("`", "")
        seg = re.sub(r"(?<!\w)\*(?!\s)", "", seg).replace("*", "")
        seg = re.sub(r"[。；;，,、\s]+$", "", seg)   # 去结尾标点
        return seg.strip()

    parts = [v for v in (_clean(x) for x in vals) if v]
    parts += [f for f in (_clean(x) for x in free_lines) if f]
    # 去重（保序）：PICOS 行与补充行可能重复同一概念
    seen, uniq = set(), []
    for p in parts:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    parts = uniq
    if not parts:
        return None
    return " ".join(parts)[:400]


def _translate_topic_authoritative(text):
    """A2 检索式翻译（关联 ct-base 权威 kw_localize，不重复造轮子）。

    ct-base 规范（references/bilingual_retrieval.md）：中文输入 → 各源「翻译前置，
    对照表优先 + miss 外接翻译 API 兜底」。本函数复用 ct-base/scripts/kw_localize.py
    的 localize_with_fallback：先查策展双语对照表（term_map），整句未译干净时
    走 online_translate 兜底（MyMemory 无密钥，可被 CT_TRANSLATE_ONLINE=0 关闭）。

    产出干净英文 query 传给 ct-literature —— 其收到纯英文后内部 topic_translator
    原样短路（无双重翻译、前后一致），从而多源（OpenAlex + Europe PMC 等）都能
    命中。返回 strategy dict 供 A2 面板如实展示（含未译残留与翻译来源）。
    """
    strategy = {
        "raw_topic": text,
        "translated_query": text,
        "untranslated": [],
        "fully_translated": True,
        "translation_hits": [],
        "source": "same",
    }
    if not text:
        return strategy
    _kw_dir = _kw_localize_scripts_dir()
    try:
        if _kw_dir not in sys.path:
            sys.path.insert(0, _kw_dir)
        import kw_localize as _k  # noqa: PLC0415  (ct-base 权威实现)
    except Exception as _e:  # noqa: BLE001  (skill 缺失/import 失败 → 原样放行，不阻断)
        # 不阻断检索，但**必须如实标注**（2026-09-17 修复）：原文本含中文却未经翻译，
        # 就不是「完整翻译」。旧实现直接返回初始值 fully_translated=True，把
        # 「中文检索式原样送国际库 → 命中偏少」这条漏检路径**伪装成正常**。
        strategy["translation_hits"] = [
            "检索式翻译模块不可用（%s）—— 请自行翻译为英文检索词：在下方"
            "「优化翻译后检索式」填入英文后重跑检索，否则中文词送境外库会明显漏检。" % _e]
        residual = re.findall(r"[\u4e00-\u9fff]+", text)
        if residual:
            strategy["untranslated"] = residual
            strategy["fully_translated"] = False
        return strategy
    en, source = _k.localize_with_fallback(text, "en")
    strategy["translated_query"] = en
    strategy["source"] = source
    residual = re.findall(r"[\u4e00-\u9fff]+", en)
    if residual:
        # 仍含中文 → 未译干净（source 应为 miss 或兜底 API 亦失败），如实标注待人工补全
        strategy["untranslated"] = residual
        strategy["fully_translated"] = False
        strategy["translation_hits"] = [
            "本地对照表未命中、外接翻译 API 也未兜底成功 —— 请自行翻译为英文检索词："
            "在下方「优化翻译后检索式」填入英文后重跑检索（残留中文送境外库会漏检）。"]
    elif source == "online":
        strategy["translation_hits"] = ["本地对照表未收全 → 外接翻译 API 兜底（ct-base "
                                        "bilingual_retrieval.md 规范）"]
    elif source == "term_map":
        strategy["translation_hits"] = ["本地策展对照表（term_map）命中"]
    return strategy


#: A2 判定口径（用户裁定 2026-09-10）：**只要核心二源均返回数据即视为 ok**。
#: 其余源（bioRxiv / arXiv / Semantic Scholar 无 key 跳过、第三方限流 429 等）缺失
#: 不再把整体降级为 error，也不触发菜单告警——它们的缺位属已知常态噪声。
CORE_SOURCES = ("OpenAlex", "EuropePMC")

# A1 选题阶段「检索数据源」可选池（规范化名）。
# 单一真源 = ct-literature `adapters/fetch_coze_unified._SOURCE_DISPLAY`（6 个走 Coze/
# 本地 fetch 的源）；此处保持一致（flow_menu.expected_sources 有同步断言）。
# ⚠️ 2026-09-11 更正：早先的 ("PubMed","Cochrane","WebOfScience","Scopus") 是错的——
#   · PubMed 并入 EuropePMC（MEDLINE/PMC 索引），非独立可检索源；
#   · Cochrane 只是 EuropePMC 的 journal-filter 子模式（ct-literature `--cochrane`），
#     不是独立源；
#   · Web of Science / Scopus 需授权 API，ct-literature 不支持。
# 另有本地专属模式（非 Coze 源，未列入本池）：PROSPERO（`--with-prospero`，token-gated）、
# Guidelines（`--with-guidelines`，需预构建本地语料库）。
AVAILABLE_SOURCES = ("OpenAlex", "EuropePMC", "bioRxiv", "medRxiv",
                     "SemanticScholar", "arXiv")


def _src_key(name):
    """来源名归一键：忽略大小写与空格 / 连字符 / 下划线差异。"""
    return re.sub(r"[\s\-_]+", "", str(name or "")).lower()


#: 来源名归一表（2026-09-17 修复「核心源误判」）：coze 统一端返回的 `studies.source`
#: 是**小写 raw key**（openalex / europepmc），本地 `fetch_*` 返回规范名
#: （OpenAlex / EuropePMC）。旧实现把 raw key 直接当 by_source 的键，与 CORE_SOURCES
#: 逐字符串比对必然失配 → 核心二源被判「全部缺位」→ search_status 误报 error
#: （实测：by_source={'openalex':13,'europepmc':3} 被判 error，实际检索成功）。
_SOURCE_CANON = {_src_key(n): n for n in AVAILABLE_SOURCES}
_SOURCE_CANON.update({
    "europepmc": "EuropePMC", "pubmed": "EuropePMC",
    "medline": "EuropePMC", "pmc": "EuropePMC",
    "semanticscholar": "SemanticScholar", "s2": "SemanticScholar",
})


def _canon_source(src):
    """归一来源名；**未知来源原样保留**（不吞信息，出现新源时人工能看见）。"""
    s = str(src or "").strip()
    if not s:
        return "unknown"
    return _SOURCE_CANON.get(_src_key(s), s)


def _a2_coverage_nha(studies, outs2, card, max_results, year_from, strategy=None):
    """A2 检索策略/覆盖确认 payload（软停）。

    展示各库条数、检索状态、撤稿数、原始主题、优化翻译后的检索式与未译残留，
    供人工闸确认。核心防「沉默漏检」：无 token 静默跳库 / skill 缺失返回空时，
    by_source 缺库 + search_status!=ok 即暴露；检索式展示优化翻译结果而非原始输入。

    判定口径（2026-09-10 用户裁定）：`search_status` 只由 CORE_SOURCES 决定 ——
    核心二源都有数据即 "ok"；核心源缺位才降级（error/partial）。原始 CLI 返回码
    另存 `cli_status` 供审计，不再直接当告警依据，避免 arXiv/无 key 源常态噪声刷屏。
    2026-09-17：来源名先经 `_canon_source` 归一（coze 端返回小写 raw key），否则核心源
    会被逐字符串比对误判为「全部缺位」而误报 error。
    """
    strategy = strategy or {}
    by_source = {}
    raw_by_source = {}   # 归一前的原始键（coze 小写 / 本地规范名），仅作审计留痕
    for s in studies:
        if isinstance(s, dict):
            raw = s.get("source") or "unknown"
            raw_by_source[raw] = raw_by_source.get(raw, 0) + 1
            src = _canon_source(raw)
            by_source[src] = by_source.get(src, 0) + 1
    status = (outs2[0].get("status") if outs2 and isinstance(outs2[0], dict) else "n/a")
    core_missing = [s for s in CORE_SOURCES if by_source.get(s, 0) <= 0]
    search_ok = (not core_missing) and len(studies) > 0
    retracted = sum(1 for s in studies if isinstance(s, dict) and s.get("is_retracted"))
    params = (card or {}).get("params") or {}
    raw_topic = strategy.get("raw_topic") or params.get("topic")
    translated_query = strategy.get("translated_query") or params.get("topic")
    untranslated = strategy.get("untranslated") or []
    fully = strategy.get("fully_translated", True)
    bits = [f"原始主题={raw_topic!r}", f"优化检索式={translated_query!r}"]
    if year_from is not None:
        bits.append(f"year≥{year_from}")
    bits.append(f"上限={max_results}")
    src_str = "、".join(f"{k}={v}" for k, v in sorted(by_source.items())) or "无来源标注"
    warn = ""
    if core_missing:
        warn = f" ⚠️ 核心源未返回：{'、'.join(core_missing)}，结果可能不完整，请核查检索配置。"
    elif not studies:
        warn = " ⚠️ 本次检索未返回任何结果，请核查检索配置。"
    prompt = (f"检索策略确认（软停）：{'; '.join(bits)} → 合并 {len(studies)} 篇（{src_str}）。"
              + warn
              + (f" 含撤稿 {retracted} 篇。" if retracted else "")
              + ("" if fully else
                 " ⚠️ 检索式未完整翻译为英文（残留：%s）：请自行翻译为英文检索词，"
                 "填入「优化翻译后检索式」后重跑检索 —— 中文词送境外库"
                 "（OpenAlex / EuropePMC）会明显漏检。"
                 % ("、".join(untranslated) or "见「未翻译残留」面板"))
              + " 请确认覆盖充分，或调整查询/库后重跑。")
    coverage = {
        "total": len(studies),
        "by_source": by_source,
        # 归一前的原始键（审计留痕）：可核对「coze 小写 raw key 已被归一」而非被丢弃
        "by_source_raw": raw_by_source,
        # 核心源口径（2026-09-10 裁定）：核心二源齐 → ok；否则 error/partial。
        "search_status": "ok" if search_ok else ("error" if status != "ok" else "partial"),
        # 原始 CLI 返回码与核心源缺位清单（审计用，不参与告警判定）
        "cli_status": status,
        "core_sources": list(CORE_SOURCES),
        "core_missing": core_missing,
        "retracted": retracted,
        "raw_topic": raw_topic,
        "query": translated_query,
        "translated_query": translated_query,
        "untranslated": untranslated,
        "fully_translated": fully,
        "translation_hits": strategy.get("translation_hits", []),
        "year_from": year_from,
        "max_results": max_results,
    }
    return {
        "type": "confirm",
        "prompt": prompt,
        "required": True,
        "gate": "none",
        "coverage": coverage,
    }


def _a2_merged_nha(cov_nha, screened, strategy=None):
    """把 A2 检索覆盖载荷 与 原 A3 初筛载荷 合并为**单节点** next_human_action。

    用户裁定（2026-09-10）：A2 检索 与 A3 初筛 **合并为一个节点**「文献集」——
    检索完即在同一节点内去重 + 规则初筛，只软停一次、只产出一张合并表。本函数是
    该节点的唯一真源：对话菜单 / 工作台 / Excel 导出与回传都读这同一份载荷。

    键位刻意保留原名，避免下游漂移：
      coverage  （原 A2）—— 供「沉默漏检」告警与检索行渲染
      summary   （原 A3）—— 三态计数 + 文献类型分布
      decisions （原 A3）—— 逐条裁决行，Excel 导出/回传的匹配锚点
    """
    screen_nha = _a3_nha_from_screened(screened)
    return {
        "type": "review",
        "required": True,
        "gate": "none",
        "prompt": (f"{cov_nha.get('prompt', '')} "
                   f"同一节点内已去重并完成规则初筛：{screen_nha.get('prompt', '')}").strip(),
        "coverage": cov_nha.get("coverage") or {},
        "search_strategy": strategy or {},
        "summary": screen_nha.get("summary") or {},
        "decisions": screen_nha.get("decisions") or [],
    }


def run_block_a(topic, max_results=50, year_from=None, debug=False,
                out_dir=".", extraction_table=None, human_decision=None,
                use_coze=False, pause_at=None,
                inclusion_hints=None, auto_fetch=True, auto_fetch_dir=None,
                max_attempts=12, pdf_email=None,
                override_query=None, a1_report_override=None,
                override_screened=None, on_line=None,
                on_a4_event=None, start_stage=None, cached_envelope=None,
                workers=4, pdf_cache_map=None, include_reviews=False,
                sources=None, pdf_dir=None):
    """本地优先 Block A 驱动器。返回与 run_pipeline 同构的 dict。

    - use_coze=False（默认）：A1/A3 走本地启发式，A2 走本地 ct-literature，A4 本地强执闸。
    - human_decision：A4 红线闸人工放行凭据 {"stage_id": A4, "action": "approved"}
      （兼容单 dict 或 list 累积凭据）。
      未提供且 A4 闸触发 → done=False / await_human=True / gate="extraction_review"。
    - pause_at：P3 软停靠集合（fullflow HITL）。算完某阶段若 sid ∈ pause_at 且未持
      对应 approved 凭据 → 提前软停（done=False / await_human=True / gate=None /
      pause=True）。默认 None = 现状行为（仅 A4 红线闸停）。
    - on_line：可选回调 f(line)，实时接收 A2 检索（ct-literature 子进程）的进度输出，
      供工作台底部信息栏展示；None = 现状行为（不转发）。
    """
    env = build_block_a_env(topic, max_results, year_from)
    pid = env["pipeline_id"]
    stages = []
    tool_card_outputs = []

    # ---- 续跑优化：start_stage ∈ {A3, A4} 且缓存信封含 A1/A2 → 跳过整块重算，
    # 直接复用已算好的早期阶段，仅跑 A3（下载）/ A4（提取）。典型场景：合并节点
    # （A2 文献集）已批准且无 revise，避免重复全库检索 + 规则初筛的分钟级无谓等待，
    # 并**保住人工在 Excel 上做的复核**（此前只在 A3 已批准时才复用 → 批准 A2 会整块重跑）。----
    # ---- 回退复用（2026-09-20）：`rewind()` 现在保留目标块的信封作为**复用源**
    # （见 FullflowSession.rewind），故 cached_envelope 在回退进 A 之后依然可用。
    # 两条复用路径都免联网：
    #   · start_stage ∈ {A3, A4}（A2 已批准且无修订）→ 直接复用 A1/A2，只跑 A3/A4（原逻辑）；
    #   · start_stage is None（回退进 A 块，A2 的 approved 已被作废）→ 比对**检索指纹**，
    #     一致则复用已检索的 studies 与 A1 查重探针，只重跑规则初筛，并在 A2 闸重新停下。
    # 指纹覆盖检索式/年限/上限/数据源/纳入综述 —— 任一改动即失效，自动回到真实联网检索。
    # 「强制重新联网检索」（前端勾选）由 fullflow 清空该信封实现，此处无需额外分支。
    _cid = ({(s.get("stage") or {}).get("id"): s
             for s in (cached_envelope.get("stages") or [])}
            if cached_envelope else {})
    _reuse_src = None
    if start_stage is None and _cid:
        _c2 = _cid.get(A2) or {}
        _c2sr = _c2.get("stage_result") or {}
        if _c2sr.get("studies") and _cid.get(A1):
            _reuse_src = {"a1": _cid.get(A1), "a2": _c2, "sr": _c2sr}

    a4_only = False
    if start_stage in ("A3", "A4") and cached_envelope:
        _s1, _s2 = _cid.get(A1), _cid.get(A2)
        if _s1 and _s2:
            _r2 = _s2.get("stage_result") or {}
            _studies = _r2.get("studies") or []
            _screened = _r2.get("screened") or []
            # 旧会话兼容：A2/A3 尚未合并时 screened 挂在独立 A3 阶段
            _s3 = _cid.get(A3)
            if not _screened and _s3:
                _screened = (_s3.get("stage_result") or {}).get("screened") or []
            if _studies or _screened:
                studies, screened = _studies, _screened
                stages = [_s1, _s2] + ([_s3] if _s3 else [])
                tool_card_outputs = []
                for _s in stages:
                    tool_card_outputs += (_s.get("tool_cards") or [])
                hints = (inclusion_hints if inclusion_hints is not None
                         else _derive_inclusion_hints(topic))
                a4_only = True

    if not a4_only:
        # A1 — 本地启发式选题 + 真实 ct-registry 查重探针（不阻塞，失败优雅降级）
        # 回退复用：同一会话内 topic 未变 → 上一轮探针仍是有效的「拥挤度快照」，
        # 直接复用跳过联网（该探针 timeout 180s，是回退进 A 块的一大块纯等待）。
        _probe_reuse = (((_reuse_src or {}).get("a1") or {}).get("stage_result") or {}).get(
            "registry_probe")
        if _probe_reuse:
            reg_probe = _probe_reuse
            if on_line:
                on_line("[A1] 复用上次 ct-registry 查重探针（跳过联网）")
        else:
            try:
                reg_probe = a1_registry_check(topic, max_results=min(max_results, 20))
            except Exception as e:  # noqa: BLE001
                reg_probe = {"status": "error", "total": None, "returned": None,
                             "sample": [], "note": f"registry 探针异常: {type(e).__name__}: {e}"}
        rep1, nha1 = a1_topic_selection(topic, registry_probe=reg_probe)
        # A1 页面「纳入综述」开关初值 = 本次 A 块配置（A1 revision 可随后覆盖）
        rep1["include_reviews"] = bool(include_reviews)
        # A1 页面「检索数据源」初值 = 本次 A 块配置（A1 revision 可随后增减）。
        # sources 是用户选题阶段选定的「要检索的库」子集；None → 用核心源全量。
        rep1["sources"] = list(sources) if sources else list(CORE_SOURCES)
        s1 = _mk_stage(A1, 0, "await_human", rep1, nha1)
        stages.append(s1)
        _st = _soft_stop(env, pid, stages, tool_card_outputs, s1, A1, pause_at, human_decision)
        if _st:
            # 复用源续存（2026-09-20）：A1 闸停靠时把缓存的 A2 阶段一并带进返回信封
            # （status 改写为 pending，故 build_state 不展示其旧结果；也正因 pending，
            # 回退选择器仍能把它当成可回退节点）。这样「打回 A1 → 未改就批准」之后，
            # A2 依旧能按检索指纹复用，不必再等 ~2 分钟全库检索。
            # 只在**真的停在 A1**时注入——A1 已批准时下面会现算出新的 s2，注入会造成
            # 同一信封出现两个 A2 阶段（重复 stage id）。
            _pending_a2 = (_reuse_src or {}).get("a2")
            if _pending_a2 and isinstance(_pending_a2.get("stage"), dict):
                _p = dict(_pending_a2)
                _p["stage"] = {**_pending_a2["stage"], "status": "pending"}
                _st["stages"] = list(_st.get("stages") or []) + [_p]
            return _st

        # A2（合并节点「文献集」）— 🟡 软停靠：检索覆盖确认 + 同节点内去重/规则初筛。
        # 用户裁定（2026-09-10）：原 A2 检索 与 A3 初筛合并为一个节点，只软停一次、
        # 只产出一张合并表（检索结果 + 裁决/理由/文献类型确认列）。
        # 检索主题优先级（2026-09-19）：A2 手改检索式 > A1 编辑版 PICOS 报告 > 原始 topic。
        # a1_report_override 由 fullflow 从 A1 revision.report 解出（_picos_report_to_query），
        # 与系统预填原文不同才注入，避免「确认未改」也覆盖主题。
        search_topic = (override_query if override_query is not None
                        else (a1_report_override or topic))
        # 检索式翻译前置（关联 ct-base 权威 kw_localize，对照表 + 外接 API 兜底）：
        # 原始中文/混合主题 → 干净英文检索式，再交给 ct-literature 多库检索。
        # 展示与真实检索都用翻译后的检索式，而非原始输入——避免「部分翻译混合串 →
        # 境外库 0 命中 → 只检索了 OpenAlex」式的沉默漏检。
        strategy = _translate_topic_authoritative(search_topic)
        # 检索指纹比对：一致 → 复用上次 studies，跳过 ct-literature 全库检索（实测约 2 分钟）。
        # 指纹不同（改了检索式 / 年限 / 上限 / 数据源 / 纳入综述）→ 走真实检索，绝不静默给旧结果。
        _fp = a2_search_fingerprint(strategy["translated_query"], max_results,
                                    year_from, include_reviews, sources)
        _cached_fp = ((_reuse_src or {}).get("sr") or {}).get("search_fingerprint")
        search_reused = bool(_reuse_src and _cached_fp and _cached_fp == _fp)
        if search_reused:
            studies = _reuse_src["sr"].get("studies") or []
            outs2, _card2 = [], None
            # coverage 载荷：prompt 按复用的 studies 现算（来源计数与实际一致），
            # 再把缓存的 coverage 盖回去，保留 search_status / cli_status 等审计字段。
            cov_nha = _a2_coverage_nha(studies, [], None, max_results, year_from,
                                       strategy=strategy)
            _cov_cached = (_reuse_src["a2"].get("next_human_action") or {}).get("coverage")
            if _cov_cached:
                cov_nha["coverage"] = _cov_cached
            cov_nha["prompt"] = ("♻ 检索输入与上次一致（指纹 %s），已**复用上次检索结果**、"
                                 "未联网重跑；如需刷新请用「强制重新联网检索」重跑本节点。 %s"
                                 % (_fp, cov_nha.get("prompt") or ""))
            if on_line:
                on_line(f"[A2] 检索指纹 {_fp} 未变 → 复用上次检索结果"
                        f"（{len(studies)} 篇，跳过联网检索）")
        else:
            studies, outs2, _card2 = a2_literature_search(
                strategy["translated_query"], max_results, year_from, out_dir,
                on_line=on_line, include_reviews=include_reviews, sources=sources)
            tool_card_outputs += outs2
            cov_nha = _a2_coverage_nha(studies, outs2, _card2, max_results, year_from,
                                       strategy=strategy)
        # 同节点内立刻初筛（摘要级纳入门控；inclusion_hints None 时由主题自动派生）
        hints = inclusion_hints if inclusion_hints is not None else _derive_inclusion_hints(topic)
        if override_screened is not None:
            # Phase 2 真接缝：直接用人工回传的逐条裁决，不重跑启发式（不覆盖人工裁决）
            screened = override_screened
        else:
            screened, _ = a3_screening(studies, inclusion_hints=hints)
        nha2 = _a2_merged_nha(cov_nha, screened, strategy)
        s2 = _mk_stage(A2, 1, "await_human",
                       {"studies": studies, "n": len(studies),
                        "coverage": cov_nha.get("coverage"),
                        "search_strategy": strategy,
                        "screened": screened, "n_screened": len(screened),
                        # 检索指纹（2026-09-20）：回退复用判据，也是审计依据
                        # （「这次结果是复用还是重跑」可回溯）。
                        "search_fingerprint": _fp,
                        "_search_reused": search_reused},
                       nha2, [_card2])
        stages.append(s2)
        _st = _soft_stop(env, pid, stages, tool_card_outputs, s2, A2, pause_at, human_decision)
        if _st:
            return _st

    # A3 — PDF 全文下载（🟡 软停；2026-09-17 用户裁定：从 A4 拆出为独立节点）
    # 刻意放在 a4_only 块之外：复用 A1/A2 缓存时（start_stage ∈ {A3, A4}）同样要执行下载。
    # 已完成（持 approved 凭据）则跳过，避免「批准 A3 后又重新下载一遍」。
    if not _any_approve(human_decision, A3):
        rep3, nha3 = a3_pdf_download(
            studies, screened, pdf_dir=(pdf_dir or auto_fetch_dir),
            max_attempts=max_attempts, inclusion_hints=hints, pdf_email=pdf_email,
            on_a4_event=on_a4_event, workers=workers, pdf_cache_map=pdf_cache_map,
        )
        s3 = _mk_stage(A3, 2, "await_human", rep3, nha3)
        stages.append(s3)
        _st = _soft_stop(env, pid, stages, tool_card_outputs, s3, A3, pause_at, human_decision)
        if _st:
            return _st

    # A4 — 数据提取（🔴 红线闸；**默认隐藏备用**：features.a4_extraction 关闭时整段跳过，
    # 流程在 A3（PDF 下载）之后即可结束，或由用户上传数据跳到 Block B）。
    # pdf_dir（2026-09-11）：A4 菜单首次出现时用户登记的本地 PDF 路径，覆盖默认缓存目录，
    # 使本地已有 PDF 优先被抽取（fullflow 从 A4 修订键 / cfg.pdf_dir 注入）。
    if features.a4_extraction_enabled():
        rep4, nha4 = a4_data_extraction(
            screened, extraction_table=extraction_table, studies=studies,
            auto_fetch=auto_fetch,
            auto_fetch_dir=(pdf_dir or auto_fetch_dir),
            max_attempts=max_attempts, inclusion_hints=hints, pdf_email=pdf_email,
            on_a4_event=on_a4_event, workers=workers, pdf_cache_map=pdf_cache_map,
        )
        s4 = _mk_stage(A4, 3, "await_human", rep4, nha4)
        stages.append(s4)

        base = {
            "pipeline_id": pid, "pipeline": env["pipeline"],
            "stages": stages, "attachments": [], "tool_card_outputs": tool_card_outputs,
        }

        gate = (s4.get("next_human_action") or {}).get("gate")
        if s4.get("_gate_blocked"):
            if _any_approve(human_decision, A4):
                return {**base, "done": True, "await_human": False, "gate": None,
                        "final": s4, "human_decisions": [human_decision]}
            return {**base, "done": False, "await_human": True, "gate": gate, "final": s4}

        return {**base, "done": True, "await_human": False, "gate": None, "final": s4}

    # 未启用 A4：Block A 以最后阶段（A3 下载 / 或缓存放行时的既有阶段）收尾
    base = {
        "pipeline_id": pid, "pipeline": env["pipeline"],
        "stages": stages, "attachments": [], "tool_card_outputs": tool_card_outputs,
    }
    return {**base, "done": True, "await_human": False, "gate": None,
            "final": stages[-1] if stages else None}
