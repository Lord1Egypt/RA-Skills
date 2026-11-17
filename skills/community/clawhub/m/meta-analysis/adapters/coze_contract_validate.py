#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adapters/coze_contract_validate.py — meta-analysis 出站信封「前置校验 + 自动修复」

两大目标（用户 2026-09-13 诉求）：
  1. 拦住装错的信封：在 POST 到 coze 之前，按 coze_contract.md 校验请求信封，
     任何不合规信封（无论来自 LLM 手搓 / 用户裸 POST / build_request 回归）
     都不会发出去，而是给出**有针对性的修正指导**。
  2. 自动修复最常见的结构错误：把「并行顶层数组」(data.yi/sei/slab 或 2×2 四列)
     重组为 coze 唯一认识的 data.rows[]；model:"random"→"REML"、measure→sm 等。

设计边界（与 coze_client / run_analysis 解耦）：
  - 纯标准库，零外部依赖；被 coze_client 在出站前调用。
  - 只读 envelope、绝不发网络、绝不改数值。
  - 修复是**保守**的：仅当结构模式清晰可识别才自动修复；识别不出 → 抛
    EnvelopeValidationError（带结构化指导），由上层转给用户，不瞎猜。

公开 API：
  validate_request(env) -> ValidationResult
      ValidationResult.ok           是否可发（修复成功且无致命问题）
      ValidationResult.issues       [Issue(...)] 所有发现（fatal/warning）
      ValidationResult.repaired    修复后的 envelope（或原样）
      ValidationResult.repaired_notes  修复动作的人类可读清单
  EnvelopeValidationError(env, result)  致命问题时抛出，带 .to_analysis() 供上层转结构化错误
  render_guidance(result) -> str        把 issues 渲染成多行指导文本（给 agent / CLI 转述）
"""
from __future__ import annotations

import copy
import json
import re

# ---------------------------------------------------------------------------
# 契约常量（对齐 coze_contract.md §3）
# ---------------------------------------------------------------------------
# task 枚举（§3）。diagnostic_meta / survival_meta 不消费 params.sm。
VALID_TASKS = frozenset({
    "pairwise_meta", "single_group_meta", "subgroup_analysis", "metareg",
    "forest_plot", "funnel_plot", "labbe_plot", "baujat_plot", "radial_plot",
    "bubble_plot", "influence", "trimfill", "nma", "nma_rank", "cnma", "survival_meta",
    "dose_resp", "diagnostic_meta", "bayesian_pairwise", "bayesian_nma",
    "gosh", "tsa", "power", "rob2", "esc", "prisma_flow", "prisma_checklist",
    "leave_one_out", "cumulative_meta", "metainc", "ipd_meta",
    "selmodel", "rve_meta", "multilevel_meta", "multivariate_meta", "nnt",
    "grade",
    # P1 架构：选题评估（不经 R 引擎，data 为上下文信封而非 rows；见 §13）
    "topic_assessment",
})

# params.model 合法值（tolower，对齐 run_task.R .meta_method / .rma_method）
VALID_MODELS_LOWER = frozenset({
    "fe", "reml", "dl", "mh", "peto", "pm", "ml", "he", "sj", "hs",
    "genq", "eb", "hk", "hakn", "knha",
})

# params.sm 合法值（对齐 §3 表；注意 ZCOR 是 has_te 分支的默认回退值，属「危险默认」）
VALID_SM = frozenset({
    "OR", "RR", "RD", "SMD", "MD", "ROM", "HR", "ZCOR",
    "IR", "IRR", "PLOGIT", "MRAW", "SENS/SPEC", "PETO",
})

# 不消费 params.sm 的 task（写 sm 属噪音，构建层会跳过；校验层同样放行）
NON_SM_TASKS = frozenset({"diagnostic_meta", "survival_meta"})

# ---------------------------------------------------------------------------
# 数据完备性（预防性阻断）配置
# ---------------------------------------------------------------------------
# 各「数据形状」的必需列别名表（**精确小写匹配**，避免 'n' 误中 'n_exp'、'y' 误中
# 'study' 这类子串误判）。一个必需列视为「存在」当且仅当：某行有该列名（精确命中
# 某别名）且至少一个单元格非空/非 NA；否则按缺失处理 → 触发预防性阻断。
_SHAPE_GROUPS = {
    "binary": {
        "event_exp": ("event_exp", "e_exp", "treatment_event", "r1", "x1", "event_t"),
        "n_exp":     ("n_exp", "treatment_n", "n_t", "n1", "tot1", "total_t"),
        "event_ctrl":("event_ctrl", "e_ctrl", "control_event", "r2", "x2", "event_c"),
        "n_ctrl":    ("n_ctrl", "control_n", "n_c", "n2", "tot2", "total_c"),
    },
    "continuous": {
        "mean_exp":  ("mean_exp", "me_exp", "y_exp", "m1", "mean_t"),
        "sd_exp":    ("sd_exp", "se_exp", "sde_exp", "sd1", "std_exp"),
        "n_exp":     ("n_exp", "treatment_n", "n_t", "n1", "tot1", "total_t"),
        "mean_ctrl": ("mean_ctrl", "me_ctrl", "y_ctrl", "m2", "mean_c"),
        "sd_ctrl":   ("sd_ctrl", "se_ctrl", "sde_ctrl", "sd2", "std_ctrl"),
        "n_ctrl":    ("n_ctrl", "control_n", "n_c", "n2", "tot2", "total_c"),
    },
    "es": {
        "te":   ("te", "yi", "logor", "logrr", "effect", "effect_size", "estimate"),
        "sete": ("sete", "sei", "se", "std_err", "standard_error", "vi"),
    },
    "single_mean": {
        "mean": ("mean", "y", "outcome", "response", "estimate"),
        "n":    ("n", "n_total", "n_exp", "sample_size", "total", "ntot"),
    },
    "single_prop": {
        "event": ("event", "events", "r", "cases", "x"),
        "n":     ("n", "n_total", "sample_size", "total", "ntot"),
    },
    "ir": {
        "event_exp": ("event_exp", "e_exp", "treatment_event", "r1", "x1"),
        "time_exp":  ("time_exp", "person_time_exp", "pt_exp", "py_exp", "time_t", "pt_t"),
        "event_ctrl":("event_ctrl", "e_ctrl", "control_event", "r2", "x2"),
        "time_ctrl": ("time_ctrl", "person_time_ctrl", "pt_ctrl", "py_ctrl", "time_c", "pt_c"),
    },
}

# 各数据形状的人类可读用途（阻断时告诉用户补什么）
_SHAPE_PURPOSE = {
    "binary":     "二分类四格表：每组需事件数(event)与样本量(n)",
    "continuous": "连续型：每组需均数(mean)、标准差(sd)、样本量(n)",
    "es":         "预计算效应量：需效应量(te)与标准误(sete)",
    "single_mean":"单组均数：需均数(mean)与样本量(n)",
    "single_prop":"单组比例：需事件数(event)与样本量(n)",
    "ir":         "发生率(人时)：每组需事件数(event)与观察人时(time)",
}

# task → 完备性策略
#   "single"        : 单组，single_mean 或 single_prop 任一完备即可
#   "strict_shape"  : 必须命中至少一个声明的标准形状（否则阻断）
#   "es_only"       : 仅接受预计算效应量形状
#   "metareg"       : strict_shape + 额外需至少一个协变量列
#   "nma"           : 网络 meta，轻量校验（需研究标识 + 干预臂 + 结局）
#   None / 其它     : 不做严格阻断（交给 coze 端校验，避免误伤冷门格式）
_COMPLETENESS_POLICY = {
    "single_group_meta": "single",
    "pairwise_meta": "strict_shape",
    "subgroup_analysis": "strict_shape",
    "metareg": "metareg",
    "bayesian_pairwise": "strict_shape",
    "dose_resp": "strict_shape",
    "multilevel_meta": "strict_shape",
    "multivariate_meta": "strict_shape",
    "rve_meta": "strict_shape",
    "ipd_meta": "strict_shape",
    "forest_plot": "es_only",
    "funnel_plot": "es_only",
    "labbe_plot": "es_only",
    "baujat_plot": "es_only",
    "radial_plot": "es_only",
    "bubble_plot": "es_only",
    "influence": "es_only",
    "trimfill": "es_only",
    "leave_one_out": "es_only",
    "cumulative_meta": "es_only",
    "gosh": "es_only",
    "nma": "nma",
    "nma_rank": "nma",
    "cnma": "nma",          # 成分网络 Meta：数据契约与 nma 完全一致（治疗标签以 sep_comps 拼接成分）
    "bayesian_nma": "nma",
}

# strict_shape 家族按此顺序尝试，取「命中必需列最多」的形状作为最佳形状
_STRICT_SHAPES = ("binary", "continuous", "ir", "es")

# 核心成对列集合（含研究标识/标签列）：metareg 检测协变量时，凡不在此集合的列名即协变量
_CORE_PAIRWISE_COLS = set()
for _g in ("binary", "continuous", "ir", "es"):
    for _aliases in _SHAPE_GROUPS[_g].values():
        _CORE_PAIRWISE_COLS.update(_aliases)
_CORE_PAIRWISE_COLS.update(("study", "label", "slab", "name", "author", "studlab", "subgroup"))

# 视为「缺失值」的标记（用于 W07 NA 扫描 + 完备性判定；仅警告，不阻断）
_NA_MARKERS = {"", "na", "n/a", "nan", "null", "none", "无", "缺失", "."}

# 并行数组 → 效应量修复：顶层可用的「效应量 / 标准误 / 标签」键名
_ES_KEYS = ("yi", "te", "TE", "logor", "logOR", "y", "effect", "effect_size")
_ESE_KEYS = ("sei", "se", "SE", "sete", "seTE", "std_err", "standard_error", "vi")
_LABEL_KEYS = ("slab", "study", "label", "name", "author", "studlab")

# 2×2 四格表修复：顶层可用的「实验组事件/样本量、对照组事件/样本量」
_BIN_EXP_E = ("event_exp", "e_exp", "treatment_event")
_BIN_EXP_N = ("n_exp", "treatment_n")
_BIN_CTRL_E = ("event_ctrl", "e_ctrl", "control_event")
_BIN_CTRL_N = ("n_ctrl", "control_n")


class Issue:
    """单条校验发现。severity: 'fatal' | 'warning'。"""

    __slots__ = ("code", "severity", "message", "fix")

    def __init__(self, code, severity, message, fix=""):
        self.code = code
        self.severity = severity
        self.message = message
        self.fix = fix

    def as_dict(self):
        return {"code": self.code, "severity": self.severity,
                "message": self.message, "fix": self.fix}


class ValidationResult:
    __slots__ = ("ok", "issues", "repaired", "repaired_notes")

    def __init__(self, ok, issues, repaired, repaired_notes=None):
        self.ok = ok
        self.issues = issues
        self.repaired = repaired
        self.repaired_notes = repaired_notes or []

    def to_dict(self):
        return {
            "ok": self.ok,
            "issues": [i.as_dict() for i in self.issues],
            "repaired_notes": self.repaired_notes,
        }


class EnvelopeValidationError(Exception):
    """出站信封致命不合规时抛出（由 coze_client 在 POST 前 raise）。

    上层（run_analysis）捕获后转成结构化错误返回，绝不把装错的信封发到 coze。
    """

    def __init__(self, env, result: ValidationResult):
        self.env = env
        self.result = result
        super().__init__(
            "出站信封校验未通过：\n" + render_guidance(result)
        )

    def to_analysis(self) -> dict:
        """供 run_analysis 直接并入返回体（_source=envelope_invalid）。"""
        fatal = [i.as_dict() for i in self.result.issues
                 if i.severity == "fatal"]
        warn = [i.as_dict() for i in self.result.issues
                if i.severity == "warning"]
        return {
            "stage": "pre_send_validation",
            "summary": "请求信封未通过 coze 契约校验，已拦截（未发送到云端）。",
            "fatal_issues": fatal,
            "warnings": warn,
            "guidance": render_guidance(self.result),
        }


# ---------------------------------------------------------------------------
# 修复
# ---------------------------------------------------------------------------
def _first_present(d: dict, keys):
    """返回 d 中首个存在的 key（区分大小写优先），否则 None。"""
    for k in keys:
        if k in d:
            return k
    return None


def _try_repair(env: dict):
    """尝试把常见装错信封修复为合规信封。

    Returns: (repaired_env_or_None, notes_list)
      - repaired_env_or_None: 修复成功返回新 envelope；否则 None（交致命问题处理）。
      - notes_list: 人类可读的修复动作清单。
    """
    data = env.get("data")
    if not isinstance(data, dict):
        return None, []
    rows = data.get("rows")
    if isinstance(rows, list) and rows:
        # 已有合法 rows：仅补 source 缺省（微小修复），其余交给 _check_contract
        if "source" not in data:
            fixed = copy.deepcopy(env)
            fixed.setdefault("data", {})["source"] = "inline"
            return fixed, ["已补 data.source='inline'（缺省推断为 inline）"]
        return None, []

    notes = []
    params = copy.deepcopy(env.get("params") or {})

    # —— 形态 A：效应量并行数组（data.yi / data.sei / data.slab …）——
    te_key = _first_present(data, _ES_KEYS)
    ese_key = _first_present(data, _ESE_KEYS)
    lab_key = _first_present(data, _LABEL_KEYS)
    if te_key and ese_key and isinstance(data[te_key], list) \
            and isinstance(data[ese_key], list) and len(data[te_key]) == len(data[ese_key]):
        te_list = data[te_key]
        ese_list = data[ese_key]
        labels = data.get(lab_key) if (lab_key and isinstance(data.get(lab_key), list)) else None
        new_rows = []
        for i in range(len(te_list)):
            lab = labels[i] if labels else "Study%d" % (i + 1)
            new_rows.append({"te": te_list[i], "sete": ese_list[i], "study": lab})
        notes.append(
            "已自动重组：并行顶层数组 data.%s / data.%s / data.%s "
            "→ data.rows[{te, sete, study}]（coze 只认 data.rows 行对象数组）"
            % (te_key, ese_key, lab_key or "<label>")
        )
        # sm：优先 params.sm，否则沿用 measure，否则按 log-OR 默认 OR
        sm = params.get("sm") or params.pop("measure", None) or "OR"
        if "sm" not in params:
            params["sm"] = sm
            notes.append("已设 params.sm='%s'（precomputed 效应量默认按 log-OR 处理；"
                         "缺失会让 coze 回退 ZCOR，合并结果失真）" % sm)
    else:
        # —— 形态 B：2×2 四格表并行数组 ——
        ee = _first_present(data, _BIN_EXP_E)
        en = _first_present(data, _BIN_EXP_N)
        ce = _first_present(data, _BIN_CTRL_E)
        cn = _first_present(data, _BIN_CTRL_N)
        if ee and en and ce and cn and isinstance(data[ee], list) \
                and len({len(data[k]) for k in (ee, en, ce, cn)}) == 1:
            n = len(data[ee])
            labels = data.get(lab_key) if (lab_key and isinstance(data.get(lab_key), list)) else None
            cols = {"event_exp": ee, "n_exp": en, "event_ctrl": ce, "n_ctrl": cn}
            new_rows = []
            for i in range(n):
                lab = labels[i] if labels else "Study%d" % (i + 1)
                row = {"study": lab}
                for canon, src in cols.items():
                    row[canon] = data[src][i]
                new_rows.append(row)
            notes.append(
                "已自动重组：2×2 四格表并行顶层数组（%s/%s/%s/%s）→ data.rows["
                "{study, event_exp, n_exp, event_ctrl, n_ctrl}]" % (ee, en, ce, cn)
            )
            if "sm" not in params:
                params.setdefault("sm", "OR")
        else:
            # 既无 rows，也无可识别的并行数组 → 无法修复
            return None, []

    # —— 参数归一 ——
    model = params.get("model")
    if isinstance(model, str):
        ml = model.strip().lower()
        if ml in ("random", "random effects", "randomeffects"):
            params["model"] = "REML"
            notes.append("model 'random' → 'REML'（coze 用 model='REML' 表示随机效应）")
        elif ml in ("fixed", "fixed effects", "fixedeffects"):
            params["model"] = "FE"
            notes.append("model 'fixed' → 'FE'（coze 用 model='FE' 表示固定效应）")
    # 丢弃非 coze 参数
    for junk in ("method",):
        if junk in params:
            params.pop(junk, None)
            notes.append("已移除 params.method（coze 无此参数；合并方法由 params.model 决定）")

    new_data = {"source": "inline", "rows": new_rows}
    if new_rows and all(set(r.keys()) == {"te", "sete", "study"} for r in new_rows):
        new_data["colmap"] = {"te": "te", "sete": "sete", "study": "study"}

    repaired = copy.deepcopy(env)
    repaired["data"] = new_data
    repaired["params"] = params
    return repaired, notes


# ---------------------------------------------------------------------------
# 数据完备性（预防性阻断）
# ---------------------------------------------------------------------------
def _nonempty(v) -> bool:
    """单元格是否算「有值」（None / 空串 / NA 标记 一律视为缺失）。"""
    if v is None:
        return False
    if isinstance(v, str):
        s = v.strip().lower()
        if s in _NA_MARKERS or s == "":
            return False
    return True


def _col_has_value(rows: list, aliases) -> bool:
    """rows 中任一行的某列（精确小写命中 aliases 之一）是否有非空/非 NA 值。"""
    al = set(aliases)
    for r in rows:
        if not isinstance(r, dict):
            continue
        for k, v in r.items():
            if str(k).lower() in al and _nonempty(v):
                return True
    return False


def _shape_missing(rows: list, group: dict) -> list:
    """返回该形状中「缺失（无列或无值）」的必需列 canon 名列表；空 = 完备。"""
    missing = []
    for canon, aliases in group.items():
        if not _col_has_value(rows, aliases):
            missing.append(canon)
    return missing


def _best_strict_shape(rows: list):
    """在 _STRICT_SHAPES 中取「命中必需列最多」的形状。

    Returns: (shape_name, missing_list, present_count)
    """
    best, best_cnt = None, -1
    for name in _STRICT_SHAPES:
        group = _SHAPE_GROUPS[name]
        present = sum(1 for a in group.values() if _col_has_value(rows, a))
        if present > best_cnt:
            best_cnt, best = present, name
    missing = _shape_missing(rows, _SHAPE_GROUPS[best]) if best else []
    return best, missing, best_cnt


def _check_single_study(task: str, rows: list, issues: list) -> None:
    """E11 致命拦截：k=1 的伪合并（飞书 searchlog 实证：1/281 成功记录 k=1）。

    依据 coze_contract.md §3：pairwise_meta / single_group_meta / subgroup_analysis
    等 task 均需 ≥2 项研究才有合并意义；k=1 时 R 端的 rma() 虽不报错但产出的
    "合并效应"实际就是单研究效应量，极易误导。出站前直接拦截。
    """
    if task not in ("pairwise_meta", "single_group_meta", "subgroup_analysis",
                     "metareg", "nma", "nma_rank", "cnma", "survival_meta", "dose_resp",
                     "ipd_meta", "bayesian_pairwise"):
        return
    if len(rows) < 2:
        issues.append(Issue(
            "E11_SINGLE_STUDY", "fatal",
            "task='%s' 仅提供 %d 项研究（需 ≥2）。k=1 的 '合并' 实为单研究效应，"
            "统计无意义且极易误导。" % (task, len(rows)),
            "补充更多研究数据；或改为森林图(forest_plot)展示单项效应量。"))


def _check_data_completeness(task: str, rows: list, issues: list) -> None:
    """预防性阻断：出站前检查数据完备性（致命 E07_DATA_INCOMPLETE）。

    设计权衡：只对「明确不完备」的情况抛 fatal，由 coze_client 在 POST 前直接打回；
    冷门/未枚举的格式不做严格阻断（交给 coze 端校验），宁可放过、绝不误杀合法请求。
    """
    policy = _COMPLETENESS_POLICY.get(task)
    if policy is None:
        return

    if policy == "single":
        miss_mean = _shape_missing(rows, _SHAPE_GROUPS["single_mean"])
        miss_prop = _shape_missing(rows, _SHAPE_GROUPS["single_prop"])
        mean_present = len(miss_mean) < 2   # 至少一个均数形状列已给
        prop_present = len(miss_prop) < 2   # 至少一个比例形状列已给
        if not mean_present and not prop_present:
            issues.append(Issue(
                "E07_DATA_INCOMPLETE", "fatal",
                "task='single_group_meta' 数据明显不完备：未匹配任何可用形状。",
                "单组 meta 需每研究提供：均数(mean)+样本量(n)，或 事件数(event)+样本量(n)。"
                "请补充对应列后重试。"))
        elif mean_present and not prop_present:
            issues.append(Issue(
                "E07_DATA_INCOMPLETE", "fatal",
                "task='single_group_meta' 采用「单组均数」格式，但缺少：%s。"
                % "、".join(miss_mean),
                "单组均数 meta 需每研究提供 mean(均数) 与 n(样本量)。"))
        elif prop_present and not mean_present:
            issues.append(Issue(
                "E07_DATA_INCOMPLETE", "fatal",
                "task='single_group_meta' 采用「单组比例」格式，但缺少：%s。"
                % "、".join(miss_prop),
                "单组比例 meta 需每研究提供 event(事件数) 与 n(样本量)。"))
        return

    if policy == "es_only":
        miss = _shape_missing(rows, _SHAPE_GROUPS["es"])
        if miss:
            issues.append(Issue(
                "E07_DATA_INCOMPLETE", "fatal",
                "task='%s' 需预计算效应量，但缺少：%s。" % (task, "、".join(miss)),
                "该任务消费已算好的效应量：请提供 te(效应量) 与 sete(标准误) 两列"
                "（可用 build_request 从原始四格表/连续型自动换算，或直接传 te/sete）。"))
        return

    if policy == "nma":
        has_study = _col_has_value(rows, ("study", "studlab", "trial", "author"))
        has_arm = _col_has_value(rows, ("treatment", "arm", "t", "comparison",
                                        "t1", "t2", "intervention", "group"))
        has_outcome = ((_col_has_value(rows, ("event", "r", "x", "cases")) and
                        _col_has_value(rows, ("n", "sample_size", "total"))) or
                       _col_has_value(rows, ("te", "yi", "effect")))
        if not (has_study and has_arm and has_outcome):
            issues.append(Issue(
                "E07_DATA_INCOMPLETE", "fatal",
                "task='%s' 未检测到完整的网络结构（研究标识 + 干预臂 + 结局）。" % task,
                "NMA 需提供：①研究列(study) ②干预臂列(treatment/arm) "
                "③结局（二分类: event+n；连续: mean+sd+n；或对比: te+se）。请按以上结构补全数据。"))
        return

    # policy in ("strict_shape", "metareg")
    best, miss, cnt = _best_strict_shape(rows)
    if cnt == 0:
        accepted = "；".join("%s（%s）" % (n, _SHAPE_PURPOSE[n]) for n in _STRICT_SHAPES)
        issues.append(Issue(
            "E07_DATA_INCOMPLETE", "fatal",
            "task='%s' 数据未匹配任何可识别格式（检测到的列均不属于标准 meta 数据形状）。" % task,
            "pairwise 类分析需提供以下之一：%s。请补充对应数据后重试。" % accepted))
    elif miss:
        issues.append(Issue(
            "E07_DATA_INCOMPLETE", "fatal",
            "task='%s' 采用「%s」格式，但缺少必需列：%s。"
            % (task, best, "、".join(miss)),
            "「%s」格式需补充：%s。" % (_SHAPE_PURPOSE[best], "、".join(miss))))
    if policy == "metareg" and not miss:
        moderator_cols = set()
        for r in rows:
            for k in r:
                if str(k).lower() not in _CORE_PAIRWISE_COLS:
                    moderator_cols.add(str(k))
        if not moderator_cols:
            issues.append(Issue(
                "E07_DATA_INCOMPLETE", "fatal",
                "task='metareg' 仅检测到效应量/四格表列，缺少调节变量（协变量）。",
                "meta 回归需至少一个调节变量列（如 age、dose、baseline 等），"
                "除研究标识与效应量/四格表列之外。请补充协变量列。"))


# ---------------------------------------------------------------------------
# 校验（针对最终 envelope）
# ---------------------------------------------------------------------------
def _check_topic_assessment(env: dict, issues: list) -> None:
    """topic_assessment 轻量结构校验（非 R 任务，data 为上下文信封）。

    仅确保关键字段类型正确，便于 coze 端 topic_assessment 节点解析；不强制 rows。
    缺字段给 warning（不阻断），让 coze 端按缺失做默认中值降级，而非出站即打回。
    """
    data = env.get("data")
    if not isinstance(data, dict):
        issues.append(Issue("W10_TOPIC_DATA", "warning",
                            "topic_assessment 的 data 应为对象（含 topic/evidence/"
                            "deterministic_scores 等）。",
                            "把选题上下文放进 data 对象。"))
        return
    if not isinstance(data.get("topic"), str) or not data.get("topic").strip():
        issues.append(Issue("W11_TOPIC_MISSING", "warning",
                            "topic_assessment 缺 topic（选题文本）；coze 端将无主题可评估。",
                            "在 data.topic 提供选题字符串。"))
    ev = data.get("evidence")
    if ev is not None and not isinstance(ev, dict):
        issues.append(Issue("W12_TOPIC_EVIDENCE", "warning",
                            "evidence 应为对象 {dedup,registry,prospero}。", ""))
    ds = data.get("deterministic_scores")
    if ds is not None and not isinstance(ds, dict):
        issues.append(Issue("W13_TOPIC_SCORES", "warning",
                            "deterministic_scores 应为对象 {method,data,novelty}。", ""))


def _check_contract(env: dict, issues: list) -> None:
    task = env.get("task")
    if not task or not isinstance(task, str):
        issues.append(Issue("E01_MISSING_TASK", "fatal",
                            "信封缺 task（任务类型）字段。",
                            "补 task，如 \"pairwise_meta\" / \"nma\" / \"subgroup_analysis\"。"))
        return
    if task not in VALID_TASKS:
        issues.append(Issue("E02_UNKNOWN_TASK", "fatal",
                            "task='%s' 不在 coze 已注册任务枚举中。" % task,
                            "合法 task 见 coze_contract.md §3（如 pairwise_meta / nma / "
                            "subgroup_analysis / metareg）。未知 task 会被 coze 返回 unknown_task。"))
        return

    # P1 架构：topic_assessment 的 data 是上下文信封（topic/picos/evidence/...），
    # 非 rows 数组，跳过 R 任务的 data.rows / 单研究 / 完备性校验，仅做轻量结构校验。
    if task == "topic_assessment":
        _check_topic_assessment(env, issues)
        return

    data = env.get("data")
    if not isinstance(data, dict):
        issues.append(Issue("E03_DATA_NOT_OBJECT", "fatal",
                            "data 必须是对象（{rows:[...]}），当前为 %s。" % type(data).__name__,
                            "把数据塞进 data.rows 数组，不要用并行顶层数组。"))
        return

    source = data.get("source", "inline")
    rows = data.get("rows")
    if not (isinstance(rows, list) and len(rows) > 0):
        issues.append(Issue("E04_MISSING_ROWS", "fatal",
                            "source=inline 时 data.rows 必须是非空对象数组；当前 data.rows=%r。"
                            % (rows,),
                            "coze R 引擎只从 data.rows 取数。把每行写成一个对象"
                            "（如 {te,sete,study} 或 {event_exp,n_exp,event_ctrl,n_ctrl,study}）"
                            "放进 data.rows。不要用 data.yi/sei/slab 这种并行顶层数组。"))
        return

    # 行必须是对象
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            issues.append(Issue("E05_ROW_NOT_OBJECT", "fatal",
                                "data.rows[%d] 必须是对象，当前为 %s。" % (i, type(r).__name__),
                                "把该行写成 {列名: 值} 对象。"))
            return

    # 列名集合（小写）
    cols = set()
    for r in rows:
        cols.update(str(k).lower() for k in r)

    # model 合法值
    params = env.get("params") or {}
    model = params.get("model")
    if model is not None:
        ml = str(model).strip().lower()
        if ml not in VALID_MODELS_LOWER:
            issues.append(Issue("E06_INVALID_MODEL", "fatal",
                                "params.model='%s' coze 不识别。" % model,
                                "合法值：FE / REML / DL / MH / Peto / PM（及 tau 估计量 "
                                "ml/he/sj/hs/genq/eb）。'random'→用 'REML'，'fixed'→用 'FE'。"
                                "注意 coze 没有 params.method 参数。"))
    # 非 coze 参数提示（warning）
    if "method" in params:
        issues.append(Issue("W01_STRAY_METHOD", "warning",
                            "params.method 不是 coze 参数，会被静默忽略。",
                            "合并方法由 params.model 决定（FE/REML/DL/...），删掉 method。"))
    if "measure" in params and "sm" not in params:
        issues.append(Issue("W02_STRAY_MEASURE", "warning",
                            "params.measure 不是 coze 参数（coze 用 params.sm）。",
                            "把 measure 改名成 sm（如 OR/RR/SMD/MD）。"))
    # sm 缺失（warning，且对 has_te 分支是「危险默认」）
    if task not in NON_SM_TASKS:
        sm = params.get("sm")
        if not sm:
            issues.append(Issue("W04_MISSING_SM", "warning",
                                "params.sm 缺失；coze has_te 分支（已给效应量）会默认回退 'ZCOR'。"
                                "若你给的是 log-OR/log-RR 等，回退 ZCOR 会让合并结果被错误反变换（失真）。",
                                "显式传 params.sm（log-OR→'OR'，log-RR→'RR'，标准化均值差→'SMD' 等）。"))
        elif str(sm).strip().upper() not in VALID_SM:
            issues.append(Issue("W05_UNKNOWN_SM", "warning",
                                "params.sm='%s' 不在已知效应量集合。" % sm,
                                "合法 sm 见 coze_contract.md §2（OR/RR/RD/SMD/MD/ROM/HR/ZCOR/IR/IRR…）。"))
    # subgroup 列必须存在于 rows
    subgroup = params.get("subgroup")
    if subgroup is not None and str(subgroup).strip():
        if str(subgroup).strip().lower() not in cols:
            issues.append(Issue("W03_SUBGROUP_COL_MISSING", "warning",
                                "params.subgroup='%s' 不在数据列 %s 中；subgroup_analysis 会静默退化为无分层主分析。"
                                % (subgroup, sorted(cols)),
                                "检查亚组列名；或把真实列名传给 subgroup。"))

    # —— 单研究伪合并拦截（E11 fatal；k=1 直接打回）——
    _check_single_study(task, rows, issues)
    # —— 数据完备性（预防性阻断，fatal；明确不完备直接打回）——
    _check_data_completeness(task, rows, issues)
    # —— 数据质量预检（警告级，不阻断合法发送）——
    _check_data_quality(task, rows, issues)


def _check_data_quality(task: str, rows: list, issues: list) -> None:
    """数据内容级预检（仅 warning，绝不 fatal）。

    目标（用户 2026-09-13 飞书 searchlog 实证）：meta 的 42 条 coze error 中，
    9 条是数据含 NA/空值 → missing value where TRUE/FALSE needed。
    这里只发警告、不阻断（避免误伤含个别缺失行的合法请求），让用户即时修正而非等 coze 报错。
    （结构性缺失已由 _check_data_completeness 的 E10 fatal 在发送前拦截。）
    """
    if not rows:
        return

    # W07：NA / 空值扫描（只扫显式缺失标记，不误伤正常字符串/数值）
    flagged = set()
    for r in rows:
        for k, v in r.items():
            if v is None:
                flagged.add(k)
                continue
            if isinstance(v, str):
                s = v.strip().lower()
                if s in _NA_MARKERS:
                    flagged.add(k)
    if flagged:
        issues.append(Issue("W07_NA_IN_DATA", "warning",
                            "data.rows 中检测到缺失值(NA/空)列：%s。coze 会报 "
                            "'missing value where TRUE/FALSE needed'。" % sorted(flagged),
                            "删除或补全含缺失值的研究行；确保数值列无空值。"))

    # W08：零单元格检测（二分类四格表中 event_exp/event_ctrl 为 0 导致 OR 极端，
    # Haldane 校正（+0.5）可能仍不理想。预警用户建议用 Peto 法。）
    # 注意：用 `is not None` 而非 `or`，避免 0 被当 falsy 跳过。
    _zero_cells = []
    for i, r in enumerate(rows):
        ee = r.get("event_exp") if "event_exp" in r else r.get("ai")
        ec = r.get("event_ctrl") if "event_ctrl" in r else r.get("ci")
        try:
            if (ee is not None and float(ee) == 0) or (ec is not None and float(ec) == 0):
                _zero_cells.append(i)
        except (TypeError, ValueError):
            pass
    if _zero_cells:
        issues.append(Issue("W08_ZERO_CELL", "warning",
                            "第 %s 行 event_exp/event_ctrl = 0（零单元格），"
                            "OR 可能极端（Haldane 校正可能仍不理想）。"
                            % ",".join(str(i+1) for i in _zero_cells),
                            "建议改用 Peto 法（sm='Peto'）或广义线性混合模型（task='ipd_meta'）。"))


# ---------------------------------------------------------------------------
# 对外入口
# ---------------------------------------------------------------------------
def validate_request(env: dict) -> ValidationResult:
    """校验（并尽力自动修复）coze 出站信封。

    Returns:
      ValidationResult:
        ok            True=可发（修复成功且无致命问题）
        issues        [Issue] 全部发现
        repaired      修复后的信封（未修复则为原样深拷贝）
        repaired_notes 修复动作清单
    """
    if not isinstance(env, dict):
        res = ValidationResult(False, [Issue("E00_NOT_OBJECT", "fatal",
                                             "envelope 必须是对象。", "")], env, [])
        return res

    repaired, repair_notes = _try_repair(env)
    work = repaired if repaired is not None else copy.deepcopy(env)

    issues = []
    _check_contract(work, issues)
    fatal = any(i.severity == "fatal" for i in issues)

    # 可发 = 无致命问题（无论是否经过自动修复）
    return ValidationResult(
        ok=(not fatal),
        issues=issues,
        repaired=work,
        repaired_notes=repair_notes,
    )


def render_guidance(result: ValidationResult) -> str:
    """把校验结果渲染成多行指导文本（给 agent / CLI 转述给用户）。"""
    lines = []
    if result.repaired_notes:
        lines.append("【已自动修复】")
        for n in result.repaired_notes:
            lines.append("  • " + n)
        lines.append("")
    if not result.issues:
        lines.append("信封校验通过，无问题。")
        return "\n".join(lines)
    fatals = [i for i in result.issues if i.severity == "fatal"]
    warns = [i for i in result.issues if i.severity == "warning"]
    if any(i.code == "E07_DATA_INCOMPLETE" for i in fatals):
        lines.append("⚠ 数据明显不完备：请求已被【直接打回】（未发送到云端）。")
        lines.append("  请按下方清单补充缺失数据后重试；不必等 coze 报错。")
        lines.append("")
    if fatals:
        lines.append("【致命问题 · 已拦截，未发送到云端】")
        for i in fatals:
            lines.append("  [%s] %s" % (i.code, i.message))
            if i.fix:
                lines.append("        → 补充数据：%s" % i.fix)
    if warns:
        lines.append("【警告 · 不影响发送，但可能导致结果失真】")
        for i in warns:
            lines.append("  [%s] %s" % (i.code, i.message))
            if i.fix:
                lines.append("        → 建议：%s" % i.fix)
    return "\n".join(lines)


# 便捷：直接拿 dict JSON 字符串校验（CLI / 调试）
def validate_json(text: str) -> ValidationResult:
    return validate_request(json.loads(text))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        try:
            env = json.load(open(sys.argv[1], encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            print("无法读取 JSON: %s" % e)
            sys.exit(1)
    else:
        env = json.load(sys.stdin)
    res = validate_request(env)
    print(render_guidance(res))
    print("\n--- repaired envelope ---")
    print(json.dumps(res.repaired, ensure_ascii=False, indent=2))
    sys.exit(0 if res.ok else 2)
