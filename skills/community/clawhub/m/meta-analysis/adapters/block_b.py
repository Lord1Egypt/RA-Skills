# -*- coding: utf-8 -*-
"""Phase 2 · Block B 管线驱动器（分析结果产出；本地只做编排 + 收发，计算上 coze）。

设计约束（对齐 contracts/pipeline_stage/v1.0.0/SPEC.md §9 / 架构终态原则 2026-09-01）：

- **coze = 唯一计算真相源**：B1 计算经 coze_client.run_stage 发往 ct-meta2 R 引擎（23 图/NMA/TSA）。
  本地不保留独立计算引擎；coze 未授权/失败 → 返回结构化错误，绝不回退本地（ct-base §5 授权门控）。
- **本地仅编排 + 收发**：本模块构造信封、调用 run_stage、消费返回 stats、驱动 B1→B2→B3→B4 阶段
  序列与 HITL 软停靠/红线闸。B1 的 pairwise 由 coze 产出，stats 经 _coze_stats_to_pairwise 映射为
  本地 pairwise 形状（对数尺度同构），供 B2/B3/B4 原样消费（零行为变更）。
- **b1_pairwise_python 仅回归/调试 oracle**（engine="local"），非运行路径，不进入发布计算。
- **NMA 暂本地 R**（b1_nma_r，待迁 coze）；B2 GRADE / B3 过度声明 / B4 质量门为本地启发式，
  同为待迁 coze 的计算大脑（见 contracts/migration）。
- B3 过度声明检测为**单点实现**，被 B4（质量门）与 C2（AI 评审，Phase 3）复用。
- 阶段序列（SPEC §9）：
    B1.meta_analysis      双范式 meta 分析（pairwise + NMA）
    B2.grade              半自动 GRADE
    B3.overclaim          过度声明检测（12 模式）
    B4.quality_gate       质量门三重（GRADE + 过度声明 + 人工闸），🔴 final_inclusion 红线
- 返回结构与 run_pipeline / run_block_a 同构：{done, await_human, gate, final, stages[],
  attachments[], tool_card_outputs[]}，便于上层统一消费。

依赖：coze_client（CONTRACT_VERSION / STAGE_SCHEMA_ID / _REDLINE_GATES / run_stage / AuthRequiredError）。
网络/R 动作在 b1_nma_r（本地 R）与 coze_client.run_stage（coze R）内部，测试可 monkeypatch。
"""

import json
import math
import os
import re
import subprocess
import tempfile
import uuid

import numpy as np

import coze_client as cc
from interpretation import interpret_result

# 本机唯一正确的 R（见用户内存 LRN：C:/Tools/R-4.6.1/bin/Rscript.exe）
R_BIN = "C:/Tools/R-4.6.1/bin/Rscript.exe"

# ---- Block B 阶段 ID（SPEC §9，严格匹配 coze 端编排对齐） ----
B1 = "B1.meta_analysis"
B2 = "B2.grade"
B3 = "B3.overclaim"
B4 = "B4.quality_gate"
BLOCK_B_SEQUENCE = [B1, B2, B3, B4]
BLOCK_B_TOTAL = len(BLOCK_B_SEQUENCE)

# 效应量零值（用于 CI 是否跨零判断）：OR/HR/RR 类零值=1，MD/SMD 类零值=0
_EFFECT_NULL = {"OR": 1.0, "HR": 1.0, "RR": 1.0, "MD": 0.0, "SMD": 0.0, "RD": 0.0}


# ---------------------------------------------------------------------------
# 信封构造（本地「prompt → 合法入参」层）
# ---------------------------------------------------------------------------
def build_block_b_env(extracted_data=None, effect_measure="OR",
                      pipeline_id=None, query_origin=None):
    env = {
        "contract_version": cc.CONTRACT_VERSION,
        "schema": cc.STAGE_SCHEMA_ID,
        "pipeline_id": pipeline_id or f"blkB-{uuid.uuid4().hex[:8]}",
        "pipeline": {"name": "block_b", "block": "B", "cfg": {}},
        "request_id": str(uuid.uuid4()),
        "task": "meta_analysis",
        "params": {"effect_measure": effect_measure},
        "stage": {"id": B1, "index": 0, "total": BLOCK_B_TOTAL,
                  "intent": "run", "prev_stage_id": None},
        "stage_context": {"human_decisions": [], "tool_card_outputs": [], "artifacts": []},
    }
    if extracted_data is not None:
        env["params"]["extracted_data"] = extracted_data
    if query_origin:
        env["query_origin"] = query_origin
    return env


# ---------------------------------------------------------------------------
# 阶段响应构造（与 parse_stage_response 输出同构）
# ---------------------------------------------------------------------------
def _mk_stage(sid, index, status, stage_result, nha, tool_cards=None):
    nha = nha or {}
    return {
        "mode": "stage",
        "stage": {"id": sid, "index": index, "total": BLOCK_B_TOTAL, "status": status,
                  "prev_stage_id": BLOCK_B_SEQUENCE[index - 1] if index > 0 else None},
        "stage_result": stage_result,
        "next_human_action": nha,
        "tool_cards": tool_cards or [],
        "_gate_blocked": bool(
            nha.get("gate") in cc._REDLINE_GATES and nha.get("required")
        ),
    }


# ---------------------------------------------------------------------------
# B1 meta 分析：pairwise（纯 Python 主引擎）+ NMA（本地 R netmeta，优雅降级）
# ---------------------------------------------------------------------------
def _study_to_te_set(study, effect_measure):
    """把单条研究归一为 (TE, seTE)。支持 2x2（事件/样本）或预计算 (TE, seTE)。"""
    if "TE" in study and "seTE" in study:
        return float(study["TE"]), float(study["seTE"])
    # 2x2 表：ai=试验组事件, bi=试验组样本, ci=对照组事件, di=对照组样本
    a = float(study.get("ai", study.get("event_e", 0)))
    b = float(study.get("bi", study.get("n_e", 0)))
    c = float(study.get("ci", study.get("event_c", 0)))
    d = float(study.get("di", study.get("n_c", 0)))
    if b <= 0 or d <= 0:
        return None
    # Haldane-Anscombe 0.5 校正避免 0 单元格
    a, c = a + 0.5, c + 0.5
    b, d = b + 0.5, d + 0.5
    if effect_measure in ("OR", "HR", "RR"):
        TE = math.log((a * d) / (b * c))
        se = math.sqrt(1.0 / a + 1.0 / b + 1.0 / c + 1.0 / d)
    else:  # 连续型 MD
        m1 = float(study.get("mean_e", 0)); m2 = float(study.get("mean_c", 0))
        s1 = float(study.get("sd_e", 0)); s2 = float(study.get("sd_c", 0))
        n1 = b; n2 = d
        TE = m1 - m2
        se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
    return TE, se


#: 比值类效应量（报告尺度 = exp(分析尺度)）。与 interpretation._RATIO_SM 同源 ——
#: 这里只作**兜底常量**，正常路径直接引用 interpretation 的那一份，避免第三份清单。
try:  # pragma: no cover - 正常总能导入
    from interpretation import _RATIO_SM as _RATIO_SM
except Exception:  # noqa: BLE001
    _RATIO_SM = frozenset({"OR", "RR", "HR", "PLO", "PLOGIT", "IRR", "RRR"})


def _stats_from_pairwise(pw, effect_measure):
    """本地 pairwise 结果 → interpretation / quality_advice 期望的 coze stats 形状。

    ⚠️ **尺度**（历史踩过的坑）：pairwise 的 TE / CI 是**对数尺度**（见 b1_pairwise_python
    docstring），而 interpretation 优先读 `pooled.estimate_exp / ci_low_exp / ci_high_exp`
    （**报告尺度**）。若不补 `_exp` 变体，比值类效应量会把 log OR 当 OR 打印
    （例如 0.481 → 印成 “合并 OR = 0.48” 而真实是 1.62）。非比值类（MD/SMD）无 exp 概念，
    原值即报告尺度，直接复用。

    返回 None 表示「不足以解读」（无 k）—— 调用方据此不下发解读卡。
    """
    if not isinstance(pw, dict) or not pw.get("k"):
        return None
    em = str(pw.get("effect_measure") or effect_measure or "").upper()
    ratio = em in _RATIO_SM

    def _exp(x):
        try:
            return math.exp(float(x))
        except Exception:  # noqa: BLE001
            return None

    te = pw.get("TE_random")
    ci = pw.get("ci_random")
    ci = list(ci) if isinstance(ci, (list, tuple)) and len(ci) == 2 else None
    pooled = {"estimate": te, "p": pw.get("p_random")}
    if te is not None:
        pooled["estimate_exp"] = _exp(te) if ratio else te
    if ci:
        pooled["ci_low"], pooled["ci_high"] = ci[0], ci[1]
        if ratio:
            pooled["ci_low_exp"], pooled["ci_high_exp"] = _exp(ci[0]), _exp(ci[1])
    return {
        "k": pw.get("k"), "sm": em, "model": "random",
        "pooled": pooled,
        "heterogeneity": {"I2": pw.get("I2"), "tau2": pw.get("tau2"), "Q": pw.get("Q")},
        "bias": {},
    }


def _interp_quality_from_stats(stats, task="pairwise_meta", params=None):
    """stats → (interpretation, quality_advice)。任一失败对应的值返回 None。

    **统一出口**（2026-09-22）：原先这段逻辑内联在 b1_meta_analysis 的 coze 成功分支里，
    local / demo 两条路径完全没有 → 工作台 B1 解读卡在那些路径恒为空。抽成一处后
    三条路径口径一致（coze 用真实 stats；local / demo 用 _stats_from_pairwise 桥接）。
    解读/评估失败**不影响主结果**（B1 数值照常返回）。
    """
    interp, qa = None, None
    try:
        _i = interpret_result(stats or {}, task, params or {})
        if _i and any(_i.values()):
            interp = _i
    except Exception:  # noqa: BLE001
        pass
    try:
        from quality_advice import evaluate_quality  # 延迟导入：规避与 block_b 的循环依赖
        _q = evaluate_quality(stats or {}, task)
        if _q and any(_q.values()):
            qa = _q
    except Exception:  # noqa: BLE001
        pass
    return interp, qa


def b1_pairwise_python(studies, effect_measure="OR"):
    """逆方差加权 pairwise meta 分析（固定+随机效应，DerSimonian-Laird）。

    ⚠️ **仅回归 / 调试 oracle（engine="local"），非运行路径**：架构终态原则（2026-09-01）规定
    coze 为唯一计算真相源，运行路径 B1 走 coze R 引擎、绝不回退本地。本函数保留作离线确定性
    回归基线 / deploy_retest 对照，不进入发布计算。

    返回 {k, TE_fixed, se_fixed, ci_fixed, p_fixed, TE_random, se_random, ci_random,
    p_random, tau2, I2, Q, forest[]}。纯 numpy，确定性、可离线测。CI 为对数尺度（TE=log OR/RR）。
    """
    pairs = []
    for s in studies:
        if not isinstance(s, dict):
            continue
        r = _study_to_te_set(s, effect_measure)
        if r is None:
            continue
        pairs.append(r)
    k = len(pairs)
    if k == 0:
        return {"k": 0, "error": "无可计算研究"}
    TE = np.array([p[0] for p in pairs], dtype=float)
    se = np.array([p[1] for p in pairs], dtype=float)
    w = 1.0 / (se ** 2)  # 固定效应权重
    # 固定效应
    TE_fe = float(np.sum(w * TE) / np.sum(w))
    se_fe = float(1.0 / math.sqrt(np.sum(w)))
    # Q 统计量与 DL 随机效应
    Q = float(np.sum(w * (TE - TE_fe) ** 2))
    df = max(k - 1, 1)
    C = float(np.sum(w) - np.sum(w ** 2) / np.sum(w))
    tau2 = max(0.0, (Q - df) / C) if C > 0 else 0.0
    w_re = 1.0 / (se ** 2 + tau2)  # 随机效应权重
    TE_re = float(np.sum(w_re * TE) / np.sum(w_re))
    se_re = float(1.0 / math.sqrt(np.sum(w_re)))
    # ⚠️ 单位：与 coze 契约一致，I2 恒为**百分数（0–100）**，不是比例。
    # （coze_contract.md §4：`stats.heterogeneity.I2` 恒为百分数；netmeta/netcomb 原生
    #   比例已在 R 引擎侧 ×100。本 oracle 必须与 _coze_stats_to_pairwise 同构 —— 二者
    #   L345 明文声明「同构」，若此处留比例会导致 B2/B3/B4 判据（I2>=75/50/25）全部假阴性。
    #   消费端（block_c / interpretation / quality_advice / writing_advisor）一律按百分数
    #   渲染，**不得二次 ×100**（否则 34.5% 会印成 3450%）。）
    I2 = max(0.0, (Q - df) / Q) * 100.0 if Q > 0 else 0.0
    z_re = TE_re / se_re
    p_re = 2 * (1 - _norm_cdf(abs(z_re)))
    z_fe = TE_fe / se_fe
    p_fe = 2 * (1 - _norm_cdf(abs(z_fe)))
    ci_re = (TE_re - 1.96 * se_re, TE_re + 1.96 * se_re)
    ci_fe = (TE_fe - 1.96 * se_fe, TE_fe + 1.96 * se_fe)
    forest = [{"TE": float(t), "seTE": float(s), "w_fixed": float(wi), "w_random": float(wri)}
              for t, s, wi, wri in zip(TE, se, w, w_re)]
    return {
        "k": k, "effect_measure": effect_measure, "engine": "python",
        "TE_fixed": TE_fe, "se_fixed": se_fe,
        "ci_fixed": [ci_fe[0], ci_fe[1]], "p_fixed": p_fe,
        "TE_random": TE_re, "se_random": se_re,
        "ci_random": [ci_re[0], ci_re[1]], "p_random": p_re,
        "tau2": tau2, "I2": I2, "Q": Q, "df": df, "forest": forest,
    }


def _norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


# 本地 R netmeta 脚本（NMA）。输入 JSON：{TE[],seTE[],t1[],t2[],studlab[],sm,reference}；输出 JSON。
# 适配 netmeta 3.6-1：参数名 TE/seTE（大写）、reference.group；NMA 结果分 .common(一致) /
# .random(不一致，netmeta 默认) 两套，须显式取其一；res$comparisons 为 "t1:t2" 标签向量。
_NMA_R_SCRIPT = r"""
library(jsonlite); library(netmeta)
# 2026-09-02：与 coze 镜像 run_task.R 一致，强制 UTF-8 locale。本地 R 默认 C locale 下
# 中文干预名（如「安慰剂」）会乱码，导致 netmeta reference.group 匹配失败；
# en_US.UTF-8 在 Windows R 4.2+ 自动映射系统 UTF-8（实测有效）。须在 fromJSON 前设置。
try(Sys.setlocale("LC_CTYPE", "en_US.UTF-8"), silent = TRUE)
try(Sys.setlocale("LC_ALL", "en_US.UTF-8"), silent = TRUE)
a <- fromJSON(commandArgs(trailingOnly=TRUE)[1])
sm <- if (is.null(a$sm)) "OR" else a$sm
ref <- if (is.null(a$reference)) NULL else a$reference
# reference.group 为 NULL 时 netmeta 3.6-1 会在 `== ""` 判定上崩（length zero），
# 故仅在非 NULL 时加入该参数（do.call 条件构造调用）。
nma_args <- list(TE = a$TE, seTE = a$seTE, treat1 = a$t1, treat2 = a$t2,
                 studlab = a$studlab, sm = sm)
if (!is.null(ref)) nma_args$reference.group <- ref
res <- do.call(netmeta, nma_args)
# 优先 random-effects NMA（netmeta 默认），回退 consistent (common)
# 2026-09-02 修复：netmeta 的 res$comparisons 为「唯一干预对」(m_unique)，
# 而 res$TE.nma.random 等按「输入对比」(m_input) 对齐——多研究共享同一对时 m_input>m_unique。
# 旧代码把二者直接 zip → "differing number of rows" 崩溃。正确做法：以输入 treat1/treat2
# (m_input) 为标签基准对齐估计向量，再按唯一干预对去重（网络估计本就是 per-pair）。
te   <- if (!is.null(res$TE.nma.random))  res$TE.nma.random  else res$TE.nma.common
sete <- if (!is.null(res$seTE.nma.random)) res$seTE.nma.random else res$seTE.nma.common
lo   <- if (!is.null(res$lower.nma.random)) res$lower.nma.random else res$lower.nma.common
hi   <- if (!is.null(res$upper.nma.random)) res$upper.nma.random else res$upper.nma.common
pv   <- if (!is.null(res$pval.nma.random)) res$pval.nma.random else res$pval.nma.common
if (length(te) == length(res$treat1)) {        # 估计向量按输入对比对齐（netmeta 3.6.x 实测）
  lbl_t1 <- res$treat1; lbl_t2 <- res$treat2
} else {                                         # 退化：估计向量按唯一对对齐
  pr <- strsplit(as.character(res$comparisons), ":")
  lbl_t1 <- sapply(pr, function(x) x[1]); lbl_t2 <- sapply(pr, function(x) x[2])
}
keep <- !duplicated(paste(lbl_t1, lbl_t2, sep = ":"))   # 唯一干预对只报一次网络估计
t1o <- lbl_t1[keep]; t2o <- lbl_t2[keep]
trx <- if (!is.null(res$trts)) res$trts else sort(unique(c(res$treat1, res$treat2)))
out <- list(
  model = if (!is.null(res$TE.nma.random)) "random" else "common",
  n_treatments = length(trx),
  treatments = trx,
  tau = if (is.null(res$tau)) NA_real_ else res$tau,
  comparisons = data.frame(t1 = t1o, t2 = t2o, TE = te[keep], seTE = sete[keep],
                           ci_low = lo[keep], ci_high = hi[keep], p = pv[keep],
                           stringsAsFactors = FALSE)
)
write_json(out, commandArgs(trailingOnly=TRUE)[2])
"""


def b1_nma_r(network_studies, effect_measure="OR", reference=None):
    """本地 R netmeta 真实 NMA。network_studies = [{t1,t2,TE,seTE,studlab}]。
    失败/缺 R/缺包 → 返回 {status:'error'/'skipped', reason}（不抛）。"""
    if not network_studies:
        return {"status": "skipped", "reason": "无网络数据"}
    try:
        data = {
            "TE": [float(s["TE"]) for s in network_studies],
            "seTE": [float(s["seTE"]) for s in network_studies],
            "t1": [str(s["t1"]) for s in network_studies],
            "t2": [str(s["t2"]) for s in network_studies],
            "studlab": [str(s.get("studlab", f"S{i}")) for i, s in enumerate(network_studies)],
            "sm": effect_measure, "reference": reference,
        }
        with tempfile.TemporaryDirectory() as td:
            inp = os.path.join(td, "nma_in.json")
            outp = os.path.join(td, "nma_out.json")
            with open(inp, "w", encoding="utf-8") as f:
                json.dump(data, f)
            rfile = os.path.join(td, "nma.R")
            with open(rfile, "w", encoding="utf-8") as f:
                f.write(_NMA_R_SCRIPT)
            proc = subprocess.run([R_BIN, rfile, inp, outp], capture_output=True,
                                 text=True, timeout=120,
                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            if proc.returncode != 0:
                return {"status": "error", "reason": f"R exit {proc.returncode}: {proc.stderr[:300]}"}
            if not os.path.isfile(outp):
                return {"status": "error", "reason": "netmeta 未产出结果文件"}
            with open(outp, encoding="utf-8") as f:
                res = json.load(f)
        return {"status": "ok", "engine": "R_netmeta", "result": res}
    except Exception as e:  # noqa: BLE001
        return {"status": "error", "reason": f"{type(e).__name__}: {e}"}


def _norm_b1_rows(studies):
    """A4/抽取产出的 ai/bi/ci/di（事件/非事件，pdf_extractor 原生） → R 引擎 metabin 约定
    event_exp/n_exp/event_ctrl/n_ctrl（事件/总数）。

    - 已含 event_exp/n_exp/event_ctrl/n_ctrl 的行原样透传（兼容演示/手动数据路径）。
    - 形如 TE/seTE 的预计算行原样透传（R 引擎单独处理）。
    - 仅含 ai/bi/ci/di 的行做换算：event_exp=ai, n_exp=ai+bi, event_ctrl=ci, n_ctrl=ci+di。
    幂等：重复调用不会重复换算（一旦已含 event_exp 即透传）。
    """
    out = []
    for s in (studies or []):
        if not isinstance(s, dict):
            out.append(s)
            continue
        if all(k in s for k in ("event_exp", "n_exp", "event_ctrl", "n_ctrl")):
            out.append(s)
            continue
        if all(k in s for k in ("ai", "bi", "ci", "di")):
            try:
                ai, bi, ci, di = (float(s["ai"]), float(s["bi"]),
                                  float(s["ci"]), float(s["di"]))
                r = dict(s)
                r["event_exp"] = ai
                r["n_exp"] = ai + bi
                r["event_ctrl"] = ci
                r["n_ctrl"] = ci + di
                out.append(r)
                continue
            except (TypeError, ValueError):
                pass
        out.append(s)
    return out


def _build_b1_coze_env(studies, effect_measure):
    """构造 B1.meta_analysis 计算阶段信封（对齐 run_analysis._build_compute_stage_env）。

    studies 经 _norm_b1_rows 归一：A4 抽取的 ai/bi/ci/di（事件/非事件）自动换算为
    R 引擎 metabin 约定的 event_exp/n_exp/event_ctrl/n_ctrl（事件/总数），实现 A4→B1 真正闭环。
    """
    return {
        "task": "pairwise_meta",
        # ⚠️ data **必须是对象** {rows:[...]}（契约 §2 / 出站校验 E03_DATA_NOT_OBJECT）：
        # 2026-09-17 修复 —— 此前直接传裸 list，被出站校验拦截（"data 必须是对象"），
        # B1 实际从未成功发出，合并计算静默落空（B 块容错继续，表面看流程照常走到 B4）。
        "data": {"rows": _norm_b1_rows(studies)},
        "params": {"effect_measure": effect_measure},
        "figure": {},
        "contract_version": cc.CONTRACT_VERSION,
        "schema": cc.STAGE_SCHEMA_ID,
        "pipeline_id": f"blkB-{uuid.uuid4().hex[:8]}",
        "pipeline": {"name": "block_b", "block": "B", "cfg": {}},
        "stage": {"id": B1, "index": 0, "total": BLOCK_B_TOTAL,
                  "intent": "run", "prev_stage_id": None},
        "stage_context": {"human_decisions": [], "tool_card_outputs": [], "artifacts": []},
        "query_origin": cc._default_query_origin(),
    }


def _extract_coze_stats(resp):
    """从 run_stage 返回信封中抽取 coze R 引擎的 stats（兼容顶层 stats 与 stage_result.result.stats）。"""
    if not isinstance(resp, dict):
        return None
    sr = resp.get("stage_result")
    if isinstance(sr, dict):
        inner = sr.get("result")
        if isinstance(inner, dict) and "stats" in inner:
            return inner["stats"]
    if "stats" in resp:
        return resp["stats"]
    return None


def _coze_stats_to_pairwise(stats, effect_measure):
    """coze R 引擎 stats → 本地 pairwise 形状（与 b1_pairwise_python 同构，CI 保持对数尺度），
    供 B2/B3/B4 原样消费，零行为变更。

    coze stats 结构：{k, model, sm, pooled:{estimate,ci_low,ci_high,p,unit,...},
    heterogeneity:{I2,tau2,H2,Q,Q_p}, bias:{...}, quality_gate:{...}}
    """
    if not isinstance(stats, dict):
        return {"k": 0, "error": "coze 未返回有效 stats"}
    pooled = stats.get("pooled") or {}
    het = stats.get("heterogeneity") or {}
    em = stats.get("sm") or effect_measure
    ci_low, ci_high, te, p = (pooled.get("ci_low"), pooled.get("ci_high"),
                              pooled.get("estimate"), pooled.get("p"))
    ci = [ci_low, ci_high] if (ci_low is not None and ci_high is not None) else None
    se = None
    if ci is not None and te is not None:
        half = (ci_high - ci_low) / 2.0
        if half > 0:
            se = half / 1.96
    return {
        "k": int(stats.get("k", 0) or 0),
        "effect_measure": em,
        "engine": "coze",
        "TE_fixed": te, "se_fixed": se,
        "ci_fixed": list(ci) if ci else None,
        "p_fixed": p,
        "TE_random": te, "se_random": se,
        "ci_random": list(ci) if ci else None,
        "p_random": p,
        "tau2": het.get("tau2"), "I2": het.get("I2"),
        "Q": het.get("Q"), "df": max(int(stats.get("k", 0) or 1) - 1, 1),
        "forest": [],
    }


def b1_meta_analysis(studies, effect_measure="OR", engine="coze", nma=False,
                     network_studies=None, nma_reference=None):
    """B1 双范式 meta 分析。

    - 默认 engine="coze"：B1 计算经 coze_client.run_stage 发往 ct-meta2 R 引擎（唯一计算真相源），
      stats 经 _coze_stats_to_pairwise 映射为本地 pairwise 形状，供 B2/B3/B4 原样消费。
      coze 未授权 / 失败 → 返回结构化错误，绝不回退本地（ct-base §5 授权门控；原则：本地不保留计算引擎）。
    - engine="local"（显式、仅回归 / 调试用，非运行路径）：走 b1_pairwise_python 本地 numpy 确定性实现。
    - NMA：nma=True 且提供 network_studies 时暂走本地 R netmeta（待迁 coze，见迁移规格）；否则 skipped。

    返回 {pairwise{...}, nma{...}, effect_measure, notes[], _source}。
    """
    notes = []
    if engine == "local":  # 回归/调试专用，非运行路径
        pairwise = b1_pairwise_python(studies, effect_measure)
        if pairwise.get("k", 0) == 0:
            notes.append("pairwise：无可计算研究（请检查 ai/bi/ci/di 或 TE/seTE 字段）。")
        nma_res = _nma_branch(nma, network_studies, effect_measure, notes, nma_reference)
        # 2026-09-22（一致性审计 P2-13）：local 路径同样产出解读卡 —— 数值是现算的，
        # 解读引擎完全能用，此前只是没人喂它 → 工作台 B1 面板恒「解读引擎未生成内容」。
        _interp, _qa = _interp_quality_from_stats(
            _stats_from_pairwise(pairwise, effect_measure), "pairwise_meta",
            {"sm": effect_measure})
        return {"effect_measure": effect_measure, "pairwise": pairwise,
                "nma": nma_res, "notes": notes, "_source": "local",
                "_interpretation": _interp, "_quality_advice": _qa}

    # 默认 coze-only（唯一计算真相源）
    try:
        env = _build_b1_coze_env(studies, effect_measure)
        resp = cc.run_stage(env)
        stats = _extract_coze_stats(resp)
        if stats is None:
            return {"effect_measure": effect_measure,
                    "pairwise": {"k": 0, "error": "coze 未返回 stats"},
                    "nma": {"status": "skipped", "reason": "B1 coze 无 stats"},
                    "notes": ["coze 响应缺 stats"], "_source": "coze_error"}
        pairwise = _coze_stats_to_pairwise(stats, effect_measure)
        if pairwise.get("k", 0) == 0:
            notes.append("pairwise：coze 返回无可计算研究。")
        nma_res = _nma_branch(nma, network_studies, effect_measure, notes, nma_reference)
        # 2026-09-20：结果解读卡（统计顾问层）——基于 coze stats 生成结构化解读，
        # 供工作台前端像对话模式那样展示「修饰和解读后的结果」。复用 run_analysis.py 同套引擎；
        # 失败不影响主结果。
        # 2026-09-22：改走统一出口 _interp_quality_from_stats（local / demo 同源，见其 docstring）。
        _interpretation, _quality_advice = _interp_quality_from_stats(
            stats, "pairwise_meta", {"sm": effect_measure})
        return {"effect_measure": effect_measure, "pairwise": pairwise,
                "nma": nma_res, "notes": notes, "_source": "coze",
                "_interpretation": _interpretation,
                "_quality_advice": _quality_advice}
    except cc.AuthRequiredError as e:
        return {"effect_measure": effect_measure, "pairwise": {"k": 0, "error": "auth_blocked"},
                "nma": {"status": "skipped", "reason": "auth_blocked"},
                "notes": [f"未授权出站（ct-base §5 授权门控）：{e}"],
                "_source": "auth_blocked", "_auth_required": True}
    except Exception as e:
        return {"effect_measure": effect_measure, "pairwise": {"k": 0, "error": f"coze_error: {e}"},
                "nma": {"status": "skipped", "reason": "coze_error"},
                "notes": [f"coze 调用失败：{type(e).__name__}: {e}"], "_source": "coze_error"}


def _nma_branch(nma, network_studies, effect_measure, notes, reference=None):
    """NMA 分支（暂本地 R netmeta，待迁 coze）。返回与旧 nma_res 同构的 dict。"""
    nma_res = {"status": "skipped", "reason": "nma=False 或未提供 network_studies"}
    if nma:
        if network_studies:
            nma_res = b1_nma_r(network_studies, effect_measure, reference=reference)
            if nma_res.get("status") != "ok":
                notes.append(f"NMA 降级：{nma_res.get('reason')}")
        else:
            notes.append("未提供 network_studies，跳过 NMA（仅 pairwise）。")
    return nma_res


# ---------------------------------------------------------------------------
# B2 半自动 GRADE（启发式；κ=0.44 仅半自动，须经人工）
# ---------------------------------------------------------------------------
def b2_grade(pairwise, risk_of_bias="moderate", indirectness="none",
             publication_bias="none"):
    """从 B1 输出 + 领域标记推导 GRADE 草表。起点 HIGH，按 5 域降级。

    降级规则（启发式，须人工确认）：
      - 不一致性：I2 >= 75% → -2（very serious），>=50% → -1（serious），>=25% → -0.5
      - 不精确：k<3 或 CI 跨零 → -1
      - 偏倚风险：high → -1，moderate → -0.5
      - 间接性：serious → -1
      - 发表偏倚：serious → -1
    返回 {grade, reasons[], domain_ratings{}}。
    """
    # 2026-09-14 防御：部分 task 的 stats 不含 pooled（如 diagnostic_meta / dose_resp /
    # bayesian_pairwise 只有 k + notes）→ ci 为 [None, None]，旧实现 `ci[0] < 1.0` 直接抛
    # TypeError，被上层 try/except 吞掉 → 这些任务的质量评估静默失效。缺失一律不参与
    # 判定（而非编造默认值），其余判据照常降级。
    def _n(v, default=None):
        try:
            return float(v)
        except (TypeError, ValueError):
            return default

    I2 = _n(pairwise.get("I2"), 0.0) or 0.0
    k = int(_n(pairwise.get("k"), 0) or 0)
    ci = pairwise.get("ci_random") or pairwise.get("ci_fixed")
    if not isinstance(ci, (list, tuple)) or len(ci) < 2:
        ci = [None, None]
    _lo_c, _hi_c = _n(ci[0]), _n(ci[1])
    _null_c = 1.0 if pairwise.get("effect_measure") in ("OR", "HR", "RR") else 0.0
    crosses_null = (_lo_c is not None and _hi_c is not None
                    and _lo_c < _null_c < _hi_c)

    # reasons 供中文工作台页面用；reasons_en 供英文稿件用（2026-09-22）。
    # 两条列表**同步 append**，任何一侧新增降级理由都必须同时补英文，否则
    # 英文稿件会漏掉该条降级说明（或回退成中文，造成中英混杂）。
    reasons = []
    reasons_en = []
    domain = {}
    down = 0.0

    # 不一致性
    if I2 >= 75:
        down += 2; domain["inconsistency"] = "very serious"
        reasons.append(f"不一致性很严重（I²={I2:.0f}% → -2）")
        reasons_en.append(f"very serious inconsistency (I²={I2:.0f}% → −2)")
    elif I2 >= 50:
        down += 1; domain["inconsistency"] = "serious"
        reasons.append(f"不一致性严重（I²={I2:.0f}% → -1）")
        reasons_en.append(f"serious inconsistency (I²={I2:.0f}% → −1)")
    elif I2 >= 25:
        down += 0.5; domain["inconsistency"] = "some"
        reasons.append(f"不一致性中等（I²={I2:.0f}% → -0.5）")
        reasons_en.append(f"moderate inconsistency (I²={I2:.0f}% → −0.5)")
    else:
        domain["inconsistency"] = "not serious"

    # 不精确
    if k < 3:
        down += 1; domain["imprecision"] = "serious"
        reasons.append(f"样本研究少（k={k} → -1）")
        reasons_en.append(f"few contributing studies (k={k} → −1)")
    elif crosses_null:
        down += 1; domain["imprecision"] = "serious"
        reasons.append("效应估计 CI 跨零（不精确 → -1）")
        reasons_en.append("confidence interval crosses the null (imprecision → −1)")
    else:
        domain["imprecision"] = "not serious"

    # 偏倚风险
    if risk_of_bias == "high":
        down += 1; domain["risk_of_bias"] = "serious"
        reasons.append("偏倚风险高（→ -1）")
        reasons_en.append("high risk of bias (→ −1)")
    elif risk_of_bias == "moderate":
        down += 0.5; domain["risk_of_bias"] = "some"
        reasons.append("偏倚风险中等（→ -0.5）")
        reasons_en.append("moderate risk of bias (→ −0.5)")
    else:
        domain["risk_of_bias"] = "not serious"

    if indirectness == "serious":
        down += 1; domain["indirectness"] = "serious"
        reasons.append("间接性严重（→ -1）")
        reasons_en.append("serious indirectness (→ −1)")
    else:
        domain["indirectness"] = indirectness

    if publication_bias == "serious":
        down += 1; domain["publication_bias"] = "serious"
        reasons.append("发表偏倚严重（→ -1）")
        reasons_en.append("serious publication bias (→ −1)")
    else:
        domain["publication_bias"] = publication_bias

    # 映射降级档位 → GRADE
    if down == 0:
        grade = "High"
    elif down <= 1:
        grade = "Moderate"
    elif down <= 2:
        grade = "Low"
    else:
        grade = "VeryLow"
    return {"grade": grade, "downgrades": down, "reasons": reasons,
            # 英文版降级理由：C1 英文稿件直接引用（与 reasons 一一对应、同序）。
            "reasons_en": reasons_en,
            "domain_ratings": domain, "coze_ready": False,
            "note": "半自动 GRADE（κ=0.44 仅半自动），须人工确认各域评级。"}


# ---------------------------------------------------------------------------
# B3 过度声明检测（12 模式；被 B4 / C2 复用）
# ---------------------------------------------------------------------------
# (pattern_id, label, severity, regex/keyword, 需 CI 跨零辅助判定)
_OVERCLAIM_PATTERNS = [
    ("OC1", "绝对化治愈/根治/革命性措辞", "high",
     r"治愈|根治|完全治愈|cure|revolutionary|breakthrough|革命性|颠覆"),
    ("OC2", "声称显著但 CI 跨零", "high",
     r"显著|显著改善|significant|明显降低|明显减少", "ci_cross"),
    ("OC3", "称无差异但 p<0.05", "high",
     r"无差异|无统计学差异|相当|no difference|equivalent", "p_sig"),
    ("OC4", "称优效但 CI 重叠（跨零）", "medium",
     r"优于|显著优于|superior|胜过", "ci_cross"),
    ("OC5", "亚组结论外推总体", "medium",
     r"亚组|subset|亚人群", "to_all"),
    ("OC6", "首个/首创声明（待核实）", "low",
     r"首个|首例|first-in-class|first"),
    ("OC7", "极端 100%/完全", "medium",
     r"100%|完全|彻底|completely|entirely"),
    ("OC8", "以 p 值替代效应量", "low",
     r"p\s*[<≤]\s*0\.0?\d+"),
    ("OC9", "事后亚组作为主要结论", "low",
     r"事后|post[- ]?hoc|探索性亚组"),
    ("OC10", "以非劣效检验不显著推断非劣", "high",
     r"非劣|non-?inferior", "ns"),
    ("OC11", "绝对安全/无副作用", "medium",
     r"安全无副作用|无副作用|safe|没有任何不良反应"),
    ("OC12", "自称 meta 分析但证据薄弱", "medium",
     r"meta|荟萃|系统评价", "weak_meta"),
]


# 同一 12 类模式的**英文**标签（2026-09-22）。
# WHY：C1 初稿是英文稿件，把中文 label 直接拼进正文会造成中英混杂；而中文
# label 是中文工作台页面的唯一真源，不能替换。故并行维护一份英文表，随 hit
# 以 `label_en` 下发，中文 label 保持不动。
_OVERCLAIM_LABEL_EN = {
    "OC1": "Absolute cure / revolutionary wording",
    "OC2": "Claims significance while the CI crosses the null",
    "OC3": "Claims no difference while p < 0.05",
    "OC4": "Claims superiority while CIs overlap (cross the null)",
    "OC5": "Subgroup finding extrapolated to the whole population",
    "OC6": "'First / first-in-class' claim (unverified)",
    "OC7": "Extreme '100% / completely' wording",
    "OC8": "p-value reported in place of an effect size",
    "OC9": "Post-hoc subgroup presented as the main conclusion",
    "OC10": "Non-inferiority inferred from a non-significant test",
    "OC11": "Absolute safety / 'no side effects' claim",
    "OC12": "Self-described meta-analysis with weak evidence",
}


# 模式图例 / 统计上下文的中文说法（B3 页面自描述用，2026-09-20）。
# 由 _OVERCLAIM_PATTERNS 的 severity / aux 字段派生，前端不硬编码任何判据文案。
_OC_SEVERITY_ZH = {"high": "高（命中即令 B4 判 critical）", "medium": "中", "low": "低"}
_OC_GUARD_ZH = {
    None: "无（纯文本命中即计入）",
    "ci_cross": "需 95% CI 跨过无效线才计入",
    "p_sig": "需合并 p<0.05 才计入",
    "ns": "需合并 p≥0.05 才计入",
    "weak_meta": "需 k<2 或 I²≥75% 才计入",
    "to_all": "命中后追加提示（亚组表述外推总体）",
}


def _overclaim_context(stats):
    """把 B1 的 pooled 统计量归一为「模式辅助判定」上下文（单点实现）。

    `detect_overclaims`（判定）与 `overclaim_stats_digest`（B3 页面展示）共用同一份判据，
    避免「判定一套、页面说明另一套」的漂移。
    2026-09-14 防御保留：ci 可能为 None（该 task 无 pooled）或含 None（网络 Meta 向量型 CI
    归一失败）；p / k / I2 亦可能缺或非数值。缺值一律取中性默认（不触发/不放过由各模式自判），
    旧实现直接参与比较会抛 TypeError。CI 是否跨零：OR/HR/RR 零值=1，MD 零值=0。
    """
    stats = stats or {}
    em = stats.get("effect_measure", "OR")
    ci = stats.get("ci_random") or stats.get("ci_fixed")
    p = stats.get("p_random") if stats.get("p_random") is not None else stats.get("p_fixed")

    def _n2(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    null = _EFFECT_NULL.get(em, 1.0)
    _clo, _chi = (None, None)
    if isinstance(ci, (list, tuple)) and len(ci) >= 2:
        _clo, _chi = _n2(ci[0]), _n2(ci[1])
    p = _n2(p)
    k = _n2(stats.get("k", 0)) or 0
    I2 = _n2(stats.get("I2", 0.0)) or 0.0
    has_ci = (_clo is not None and _chi is not None)
    return {
        "effect_measure": em, "null_value": null,
        "ci_lo": _clo, "ci_hi": _chi, "has_ci": has_ci,
        "p": p, "has_p": p is not None, "k": k, "I2": I2,
        "ci_cross": (has_ci and _clo < null < _chi),
        "p_sig": (p is not None and p < 0.05),
        "is_ns": (p is not None and p >= 0.05),
        # meta 证据薄弱：研究少或异质性极大（原 `k >= 2 and I2 < 75` 取反，等价）
        "weak_evidence": (k < 2 or I2 >= 75),
    }


def detect_overclaims(claims_text, stats=None):
    """检测文本中的过度声明（12 模式）。stats 来自 B1：{effect_measure, ci_random/ci_fixed,
    p_random/p_fixed, k, I2}。返回命中列表 [{id,label,severity,evidence}]（被 B4/C2 复用）。"""
    ctx = _overclaim_context(stats)
    text = (claims_text or "").lower()
    hits = []
    for pid, label, sev, patt, *aux in _OVERCLAIM_PATTERNS:
        if not re.search(patt, text, re.IGNORECASE):
            continue
        aux_kind = aux[0] if aux else None
        evidence = label
        if aux_kind == "ci_cross" and not ctx["ci_cross"]:
            continue  # 需 CI 跨零但并未跨零 → 不误报
        if aux_kind == "p_sig" and not ctx["p_sig"]:
            continue
        if aux_kind == "ns" and not ctx["is_ns"]:
            continue
        if aux_kind == "weak_meta" and not ctx["weak_evidence"]:
            continue
        if aux_kind == "to_all" and "总体" not in text and "all" not in text and "整体" not in text:
            evidence += "（文中含亚组表述，请确认是否外推总体）"
        hits.append({"id": pid, "label": label, "severity": sev, "evidence": evidence,
                     "label_en": _OVERCLAIM_LABEL_EN.get(pid, label)})
    return hits


def overclaim_pattern_legend():
    """12 类模式的图例：B3 页面用来说明「到底查了什么」（单一真源 = _OVERCLAIM_PATTERNS）。"""
    out = []
    for pid, label, sev, patt, *aux in _OVERCLAIM_PATTERNS:
        aux_kind = aux[0] if aux else None
        out.append({
            "id": pid,
            "label": label,
            "severity": sev,
            "severity_zh": _OC_SEVERITY_ZH.get(sev, sev),
            "guard": _OC_GUARD_ZH.get(aux_kind, aux_kind or "—"),
            "regex": patt,
        })
    return out


def overclaim_stats_digest(stats):
    """B3 页面「本次可用的统计判定条件」：把 _overclaim_context 翻译成可读值。

    目的：让「为什么没命中」可解释 —— 若某条辅助条件缺失（如无 pooled CI），
    依赖它的模式本次**根本无法触发**，页面必须说清楚，不能让人误读成「没风险」。
    """
    ctx = _overclaim_context(stats)
    em, null = ctx["effect_measure"], ctx["null_value"]
    if ctx["has_ci"]:
        ci_txt = "%.4g ~ %.4g" % (ctx["ci_lo"], ctx["ci_hi"])
        cross_txt = "是（跨过 %g → 合并结论不稳健）" % null if ctx["ci_cross"] else "否"
    else:
        ci_txt, cross_txt = "—（本次无合并 CI）", "无法判定（缺 CI，依赖它的模式已跳过）"
    p_txt = ("%.4g" % ctx["p"]) if ctx["has_p"] else "—（本次无合并 p 值）"
    guards = []
    guards.append("CI 跨零：" + ("满足" if ctx["ci_cross"] else "不满足"))
    guards.append("p<0.05：" + ("满足" if ctx["p_sig"] else "不满足"))
    guards.append("p≥0.05：" + ("满足" if ctx["is_ns"] else "不满足"))
    guards.append("证据薄弱（k<2 或 I²≥75%）：" + ("满足" if ctx["weak_evidence"] else "不满足"))
    return {
        "effect_measure": em,
        "null_value": null,
        "ci": ci_txt,
        "ci_cross": cross_txt,
        "p": p_txt,
        "k": ctx["k"],
        "I2": ctx["I2"],
        "guards": "；".join(guards),
    }


# ---------------------------------------------------------------------------
# B4 质量门三重（🔴 final_inclusion 红线，本地强执）
# ---------------------------------------------------------------------------
def b4_quality_gate(grade_report, overclaims):
    """质量门三重：GRADE + 过度声明 + 人工闸。

    始终产出 🔴 final_inclusion 人工闸（required=True）；若存在 high 级过度声明或 GRADE=VeryLow，
    标记 critical=True（必须人工显式批准方可放行，自动续跑被阻断）。
    """
    grade = grade_report.get("grade", "Low")
    high = [h for h in overclaims if h.get("severity") == "high"]
    critical = bool(high) or grade == "VeryLow"
    n_med = len([h for h in overclaims if h.get("severity") == "medium"])
    _dr = grade_report.get("domain_ratings") or {}
    report = {
        "grade": grade,
        "n_overclaim": len(overclaims),
        "n_high": len(high),
        "n_medium": n_med,
        "critical": critical,
        "coze_ready": False,
        "note": "质量门三重：GRADE + 过度声明 + 人工闸。须人工显式批准方可进入 Block C 撰写。",
        # 2026-09-17 用户要求：「这一步显示的内容最好加以解释」。把 GRADE 的降级理由与五个
        # 维度评级**展开为顶层标量**（前端 object 面板直接可读，不依赖嵌套 path 支持），
        # 避免只显示一句 grade=Low 让人不知依据。
        "grade_downgrades": grade_report.get("downgrades"),
        "grade_reasons_text": ("；".join(grade_report.get("reasons") or []) or "无降级"),
        "domain_risk_of_bias": _dr.get("risk_of_bias"),
        "domain_inconsistency": _dr.get("inconsistency"),
        "domain_indirectness": _dr.get("indirectness"),
        "domain_imprecision": _dr.get("imprecision"),
        "domain_publication_bias": _dr.get("publication_bias"),
        "overclaim_hits": overclaims[:10],
    }
    nha = {
        "type": "approve",
        "prompt": (f"质量门（final_inclusion）：GRADE={grade}，检出过度声明 {len(overclaims)} 条"
                   f"（high={len(high)}）。{'存在高危过度声明或极低质量证据，' if critical else ''}"
                   f"请人工核验后批准进入 Block C。"),
        "required": True,
        "gate": "final_inclusion",
    }
    return report, nha


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
# 编排：B1 → B2 → B3 → B4（本地优先）
# ---------------------------------------------------------------------------
def run_block_b(studies, effect_measure="OR", nma=False, network_studies=None,
                claims_text=None, grade_inputs=None, debug=False,
                human_decision=None, pause_at=None, claims_meta=None):
    """Block B 驱动器（coze 计算 + 本地编排）。返回与 run_pipeline 同构的 dict。

    B1 计算上 coze（b1_meta_analysis 默认 engine="coze"）；B2/B3/B4 为本地启发式
    （待迁 coze，见 contracts/migration）。

    - human_decision：B4 红线闸人工放行凭据 {"stage_id": B4, "action": "approved"}
      （兼容单 dict 或 list 累积凭据）。
      未提供且 B4 闸触发 → done=False / await_human=True / gate="final_inclusion"。
    - pause_at：P3 软停靠集合（fullflow HITL）。默认 None = 现状行为（仅 B4 红线闸停）。
    - claims_meta（2026-09-20）：B3 输入的**来源说明**（谁拼的这段被扫文本），由上层
      （fullflow `_build_claims_text`）产出，透传进 B3 stage_result 供页面自证；
      缺省 None 时页面显示「未提供来源说明」，不阻断检测。
    """
    env = build_block_b_env(studies, effect_measure)
    pid = env["pipeline_id"]
    stages = []

    # 2026-09-19：B1 无数据（A3 强制进入 B 但未上传/提取）→ 以「待补数据」停靠，
    # 不调用 coze 合并计算、不级联到 C；前端在 B1 内提供上传/录入入口，上传后就地重算。
    if not studies:
        s1 = _mk_stage(B1, 0, "await_human",
                       {"pairwise": {"k": 0, "effect_measure": effect_measure,
                                     "notes": ["B1 合并计算需要数据：请在下方上传/录入 2×2 数据后重算。"]},
                        "nma": {"status": "skipped", "reason": "无数据"},
                        "effect_measure": effect_measure},
                       {"type": "review", "required": True, "gate": None,
                        "await_data": True,
                        "prompt": ("B1 合并计算需要数据：请上传或粘贴 2×2 数据"
                                   "（首行表头 study, ai, bi, ci, di 或 te/sete），提交后就地重算。")})
        return {"done": False, "await_human": True, "stages": [s1],
                "attachments": [], "tool_card_outputs": [], "final": s1, "gate": None}

    # B1（coze 计算；engine="coze" 为唯一运行路径，绝不回退本地）
    b1 = b1_meta_analysis(studies, effect_measure, engine="coze", nma=nma,
                          network_studies=network_studies)
    s1 = _mk_stage(B1, 0, "completed", {"pairwise": b1["pairwise"], "nma": b1["nma"],
                                         "effect_measure": effect_measure,
                                         "_interpretation": b1.get("_interpretation"),
                                         "_quality_advice": b1.get("_quality_advice")},
                   # 2026-09-17：B1 也会软停（DEFAULT_PAUSE_AT 含 B1.meta_analysis）——
                   # 停靠时前端取 nha.prompt 作为提示语，故必须给出（此前为 None → 空提示）。
                   {"type": "review", "required": True, "gate": "none",
                    "prompt": ("合并计算完成：请核对下方合并效应量、95% CI 与异质性（I² / τ²）。"
                               "确认后点「批准 / 放行」继续进入 GRADE 分级与质量门。")})
    stages.append(s1)
    _st = _soft_stop(env, pid, stages, s1, B1, pause_at, human_decision)
    if _st:
        return _st

    # B2
    gi = grade_inputs or {}
    grade_rep = b2_grade(b1["pairwise"],
                        risk_of_bias=gi.get("risk_of_bias", "moderate"),
                        indirectness=gi.get("indirectness", "none"),
                        publication_bias=gi.get("publication_bias", "none"))
    s2 = _mk_stage(B2, 1, "completed", grade_rep, None)
    stages.append(s2)
    _st = _soft_stop(env, pid, stages, s2, B2, pause_at, human_decision)
    if _st:
        return _st

    # B3（stats 来自 B1 pairwise）
    pw = b1["pairwise"]
    stats = {"effect_measure": effect_measure,
             "ci_random": pw.get("ci_random"), "ci_fixed": pw.get("ci_fixed"),
             "p_random": pw.get("p_random"), "p_fixed": pw.get("p_fixed"),
             "k": pw.get("k"), "I2": pw.get("I2")}
    overclaims = detect_overclaims(claims_text or "", stats)
    # 2026-09-20：B3 页面自描述字段（用途 / 原理 / 输入 / 去向）。
    # 由 _OVERCLAIM_PATTERNS + _overclaim_context + claims_meta 派生 → 页面文案与判据同源，
    # 不会出现「说明写一套、判定跑另一套」。旧字段 n_patterns / n_hits / hits 原样保留
    # （B4、C2、保存的旧会话均按原名消费，零行为变更）。
    _by_sev = {"high": 0, "medium": 0, "low": 0}
    for _h in overclaims:
        if _h.get("severity") in _by_sev:
            _by_sev[_h["severity"]] += 1
    _cm = claims_meta if isinstance(claims_meta, dict) else {}
    _n_chars = len(claims_text or "")
    _is_empty = not (claims_text or "").strip()
    _n_stu = _cm.get("n_studies") or 0
    _stu_total = _cm.get("studies_total")
    if _is_empty:
        _cov = "本次送检文本为空 —— 12 类文本模式全部无从触发。"
        _note = ("⚠ 0 命中 ≠ 无风险：上游（A 块检索）没有产出可比对的标题/摘要，"
                 "不是「扫了没发现」。")
    else:
        _cov = ("选题 + A2 检索结果前 %d 篇的标题/摘要" % _n_stu) if _n_stu else "未提供篇目构成"
        if _stu_total and _stu_total > _n_stu:
            _cov += "（A2 共 %d 篇，仅前 %d 篇进入比对）" % (_stu_total, _n_stu)
        _note = "已比对 %d 字。" % _n_chars
    s3 = _mk_stage(B3, 2, "completed", {
        "n_patterns": len(_OVERCLAIM_PATTERNS),
        "n_hits": len(overclaims),
        "hits": overclaims,
        # 分级计数同时给「嵌套」（供程序消费）与「平铺」（object 面板字段只认平铺键）
        # 两套读法，均由同一个 _by_sev 派生 → 不会漂移。
        "by_severity": _by_sev,
        "n_high": _by_sev["high"], "n_medium": _by_sev["medium"], "n_low": _by_sev["low"],
        "patterns": overclaim_pattern_legend(),
        "scan": {
            "source": _cm.get("source") or ("（未提供来源说明：直接调用 run_block_b 时无上层元信息）"),
            "coverage": _cov,
            "chars": _n_chars,
            "n_studies": _n_stu,
            "note": _note,
            "preview": (claims_text or "")[:600],
            "truncated": _n_chars > 600,
        },
        "stats_used": overclaim_stats_digest(stats),
        "downstream": (
            "命中 high → B4 质量门判 critical（必须人工显式放行，自动续跑被阻断）；"
            "全部命中同时被 C2 AI 评审复用。"
        ),
    }, None)
    stages.append(s3)
    _st = _soft_stop(env, pid, stages, s3, B3, pause_at, human_decision)
    if _st:
        return _st

    # B4 — 🔴 红线闸
    b4_rep, nha4 = b4_quality_gate(grade_rep, overclaims)
    # 2026-09-17 修复「质量报告 null」：前端 B4 面板读 `editable.report`
    # （EDITABLE_KEYS["B4.quality_gate"]=["report"]，_view 从 stage_result 同名键取），
    # 而 b4_quality_gate 返回的是**平铺** dict（grade / n_overclaim / ...）→ 取不到。
    # 此处同时提供平铺键与嵌套 report，两种读法都兼容。
    s4 = _mk_stage(B4, 3, "await_human", {**b4_rep, "report": dict(b4_rep)}, nha4)
    stages.append(s4)

    base = {
        "pipeline_id": pid, "pipeline": env["pipeline"],
        "stages": stages, "attachments": [], "tool_card_outputs": [],
    }

    gate = (s4.get("next_human_action") or {}).get("gate")
    if s4.get("_gate_blocked"):
        if _any_approve(human_decision, B4):
            return {**base, "done": True, "await_human": False, "gate": None,
                    "final": s4, "human_decisions": [human_decision]}
        return {**base, "done": False, "await_human": True, "gate": gate, "final": s4}

    return {**base, "done": True, "await_human": False, "gate": None, "final": s4}


# ---------------------------------------------------------------------------
# 演示用 Block B 信封（2026-09-22 用户要求）
# ---------------------------------------------------------------------------
#: 首页选「已备好 B 信封 → 跳至 C 撰稿」却**未提供任何信封**时，用这份示例继续流程，
#: 作为 Block C（C1 初稿 → C2 AI 评审 → C3 参考核验 → C4 证据 QA）的演示输入。
#:
#: **结果不硬编码**：B1-B4 一律用本模块真实函数现算（b1_pairwise_python / b2_grade /
#: detect_overclaims / b4_quality_gate），保证合并效应量、GRADE、过度声明、质量门
#: 四者互相自洽 —— 改了示例研究，下游摘要跟着一起变，不会出现「OR 显著但 GRADE 说
#: CI 跨零」这类自相矛盾的假数据。与 block_a.DEMO_RAW_CSV 同一思路：演示数据也是真算出来的。
DEMO_B_STUDIES = [
    {"study": "Study A", "ai": 26, "bi": 120, "ci": 48, "di": 118},
    {"study": "Study B", "ai": 20, "bi": 96, "ci": 35, "di": 98},
    {"study": "Study C", "ai": 16, "bi": 74, "ci": 29, "di": 76},
    {"study": "Study D", "ai": 38, "bi": 150, "ci": 58, "di": 148},
    {"study": "Study E", "ai": 11, "bi": 58, "ci": 21, "di": 60},
    {"study": "Study F", "ai": 33, "bi": 90, "ci": 23, "di": 92},
]

#: 演示「被扫描的文本」（B3 的输入）。刻意含一处**会被命中的**措辞（亚组外推总体），
#: 让 B3 有 1 条中危命中 → B4 显示 n_overclaim=1 但 critical=False（不阻断 C 流程），
#: 同时给 C2 AI 评审一条可复用的线索。
DEMO_B_CLAIMS_TEXT = (
    "本系统评价共纳入 6 项随机对照试验（合计 902 名受试者），评估干预对主要结局的影响。"
    "合并结果显示干预组主要结局发生风险低于对照组，各研究效应方向总体一致。"
    "亚组分析提示在基线风险较高的人群中效应更为明显。"
)

#: 演示用**英文**题名（2026-09-22）。
#: WHY：C1 初稿正文是英文，而演示信封的效应量/GRADE 是按下面这个主题（omega-3
#: 补充 vs 成人抑郁症状）现算的。若调用方只传中文主题，英文句子里直接嵌中文会
#: 造成中英混杂，故演示路径配套给一个英文题名。
DEMO_TOPIC_EN = (
    "Efficacy of omega-3 (DHA) supplementation on depressive symptoms in adults: "
    "a systematic review and meta-analysis of randomized controlled trials"
)


def demo_b_env(effect_measure="OR"):
    """构造演示用 Block B 信封（与 run_block_b 同构；done=True / await_human=False）。

    每次返回**新建** dict，调用方可安全改写；构造失败返回 None，由调用方决定兜底
    （演示数据不得抛异常打断启动流程）。
    """
    try:
        pw = b1_pairwise_python(DEMO_B_STUDIES, effect_measure)
        if not pw.get("k"):
            return None
        grade_rep = b2_grade(pw, risk_of_bias="moderate")
        overclaims = detect_overclaims(DEMO_B_CLAIMS_TEXT, stats=pw)
        b4_rep, _nha4 = b4_quality_gate(grade_rep, overclaims)
        _by_sev = {"high": 0, "medium": 0, "low": 0}
        for _h in overclaims:
            if _h.get("severity") in _by_sev:
                _by_sev[_h["severity"]] += 1
        _n_chars = len(DEMO_B_CLAIMS_TEXT)
    except Exception:  # noqa: BLE001 — 演示数据异常不得抛出，交给调用方兜底
        return None

    # 2026-09-22（一致性审计 P2-13）：演示信封此前不带 _interpretation / _quality_advice，
    # 导致演示模式下 B1「结果解读」面板显示「（解读引擎未生成内容）」—— 而演示的数值是
    # 现算的，解读引擎本可用。现补上，形状与 run_block_b 的 S1 对齐。
    _interp_d, _qa_d = _interp_quality_from_stats(
        _stats_from_pairwise(pw, effect_measure), "pairwise_meta", {"sm": effect_measure})
    s1 = _mk_stage(B1, 0, "completed", {
        "pairwise": pw, "effect_measure": effect_measure,
        "nma": {"status": "skipped", "reason": "demonstration envelope: no network meta-analysis performed"},
        "_interpretation": _interp_d,
        "_quality_advice": _qa_d,
    }, None)
    s2 = _mk_stage(B2, 1, "completed", grade_rep, None)
    s3 = _mk_stage(B3, 2, "completed", {
        "n_patterns": len(_OVERCLAIM_PATTERNS),
        "n_hits": len(overclaims), "hits": overclaims,
        "by_severity": _by_sev,
        "n_high": _by_sev["high"], "n_medium": _by_sev["medium"], "n_low": _by_sev["low"],
        "patterns": overclaim_pattern_legend(),
        "scan": {
            "source": "演示信封（内置示例文本，非真实检索结果）",
            "coverage": "内置示例文本 %d 字" % _n_chars,
            "chars": _n_chars, "n_studies": len(DEMO_B_STUDIES),
            "note": "已比对 %d 字（演示数据）。" % _n_chars,
            "preview": DEMO_B_CLAIMS_TEXT[:600],
            "truncated": _n_chars > 600,
        },
        "stats_used": overclaim_stats_digest(pw),
        "downstream": ("命中 high → B4 质量门判 critical（必须人工显式放行，自动续跑被阻断）；"
                       "全部命中同时被 C2 AI 评审复用。"),
    }, None)
    # 与 run_block_b 一致：B4 同时给平铺键与嵌套 report（前端 B4 面板读 editable.report）
    s4 = _mk_stage(B4, 3, "completed", {**b4_rep, "report": dict(b4_rep)}, None)
    return {
        "pipeline_id": "demo-b-env", "pipeline": "B",
        "stages": [s1, s2, s3, s4],
        "attachments": [], "tool_card_outputs": [],
        "done": True, "await_human": False, "gate": None, "final": s4,
        "_demo": True,
        "note": "内置示例 B 信封（演示）：数值由 Block B 本地函数现算，仅用于跑通 Block C 流程。",
    }
