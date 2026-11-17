#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_request.py — meta-analysis 技能「计算轨」归一化/装配脚本

设计目标（对齐 §0 双轨门控 + 延迟不变量）：
  - 一次本地调用同时完成：classify（轨道/任务判定）+ 数据归一化 + 装配 run_analysis 的
    request.json。火前本地工具调用硬压到 1 次，彻底消灭「LLM 手写 request.json + 再翻文档确认列名」。
  - 零 LLM 决策：轨道/任务/measure/model 全部来自 classify.py 关键词表（确定性）。
  - 零计算：仅做字符串/JSON 处理，绝不跑 R / Python 算任何统计量。
  - 零出网：纯本地，产出 request.json 供下一步 run_analysis 转发 coze。

输入（CLI）：
  --query "..."        用户原始请求（内部调用 classify.py 出 spec；与 --spec 二选一）
  --spec spec.json     预生成的 classify 输出（跳过 query→classify）
  --data path.csv/.json   研究数据文件（CSV 或 JSON：行数组 / {"rows":[...]}）
  --data-json '[...]'     研究数据内联 JSON（行数组 / {"rows":[...]}），免写文件
  --out request.json  输出路径（默认 request.json）

输出：run_analysis 可直接吃的 request.json
  {
    "task": "pairwise_meta" | ...,
    "data": {"rows":[...], "colmap":{列:列}},
    "params": {"sm":"OR", "model":"REML", "common":false, "random":true, "subgroup":...},
    "figure": {"plots":["forest", ...]},
    "query_origin": "sha256:<64hex>"   // 调用方约束：产物可直接 POST /run，不产生空归因
  }

红线：
  - 选题轨（spec.track=="topic"）→ 直接报错退出，本脚本只服务计算轨。
  - 缺数据字段 → 报错并列出缺的列，不静默补空。
  - 列名不匹配 → 先别名自动匹配；仍解析不出 → 发结构化 `needs_llm_fallback` JSON（exit 2），
    由 LLM 最小判断后用 `--colmap` 回灌重跑（**有边界兜底，不破默认快路径**）。
  - 不翻译/不改写任何数值；只搬运列名与 task/measure/model。
"""
import sys
import os
import re
import json
import csv
import argparse

# 让 classify 可被直接 import（与 build_request 同目录）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from classify import classify as _classify
except ImportError:  # 平铺执行
    sys.path.insert(0, os.getcwd())
    from classify import classify as _classify

# 用户语言检测（user_language 备用入参）：复用 ct-base 共享底座 i18n，不再自带重复实现。
# 用 importlib 以别名加载 ct-base/scripts/i18n.py，避免与本技能自带 scripts/i18n.py（UI 提示文案）撞名。
# 判定优先级（ctbase_i18n.resolve_user_language）：① 显式 --language 最高；② 否则按【输入 query 文本】
# 判定（含 CJK→zh，纯英文→en），解决"中文系统 + 英文输入"误判 zh 盲区；③ query 为空回退系统 locale。
# 详见 ct-base/references/language_policy.md。
import importlib.util as _ilu

_HERE = os.path.dirname(os.path.abspath(__file__))
_CTBASE_I18N_PATH = os.path.normpath(
    os.path.join(_HERE, "..", "..", "ct-base", "scripts", "i18n.py")
)
try:
    _spec = _ilu.spec_from_file_location("_ctbase_i18n", _CTBASE_I18N_PATH)
    ctbase_i18n = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(ctbase_i18n)
except Exception:
    ctbase_i18n = None

# 调用方约束（2026-08-30）：build 产物 request.json 也要带有效 query_origin，
# 即使被人手直接 POST /run 也不产生空归因（复用 coze_client 的唯一实现）。
_adapters = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "adapters")
if _adapters not in sys.path:
    sys.path.insert(0, _adapters)
try:
    from coze_client import _default_query_origin as _origin
except Exception:  # noqa: BLE001 — 极端情况下回退内联实现，绝不阻断装配
    import hashlib as _hashlib
    import socket as _socket
    def _origin(debug: bool = False) -> str:
        try:
            _h = _socket.gethostname() or "unknown"
        except Exception:  # noqa: BLE001
            _h = "unknown"
        _d = _hashlib.sha256(_h.encode("utf-8")).hexdigest()
        return ("debug:sha256:" if debug else "sha256:") + _d


# measure/model → coze params 映射（对齐 run_analysis 契约：params.sm / params.model）
MODEL_MAP = {
    "REM-L": ("REML", False, True),   # model, common, random
    "MH": ("MH", True, False),
}
# 各 task 的默认出图（对齐 coze_contract.md §3 + adapters/coze_cases 实测）。
#
# 设计原则（2026-08-27 整理）：
#   1) 有专属图名且 coze 认该名 → 显式列名（如 nma→netgraph+netleague、tsa→tsa）。
#   2) coze 端按 task 自动渲染主图、参考 case 用 `plots:[]` 触发者
#      （nma_rank / dose_resp / selmodel / rve_meta / multilevel_meta /
#       multivariate_meta / nnt / esc / prisma_checklist / grade / leave_one_out /
#       cumulative_meta / drapery / tsa / power / rob2 / prisma_flow / gosh）→ 登记为 []，
#       由 coze 按 task 自渲染**该 task 的恰当主图/表格**，**绝不强行森林图**。
#       注意（2026-08-28 修正）：`influence` 不在该组——coze 端 `if ("influence" %in% plots)`
#       才出图，故 DEFAULT_PLOTS["influence"] 须显式给 ["influence"]，不能留空。
#       这是旧版 `DEFAULT_PLOTS.get(task, ["forest"])` 兜底的最大隐患：
#       未登记方法一律被塞森林图，覆盖掉 coze 自身更合适的默认。
#   3) pairwise_meta 默认 forest+funnel+baujat+radial；**二元结局**（OR/RR/RD/IR/IRR/PETO）
#      再追加 labbe+trimfill（labbe/trimfill 仅二元 2×2 适用，连续型自动跳过，避免空图）。
#      注：loo/gosh/cumulative 属派生专属 task（不同 R 对象），不可并入 pairwise_meta，
#      须各自 task 触发（coze 端对 pairwise_meta 里的 loo 会静默忽略，已实测）。
#   4) 兜底改为 `[]`：任何未登记 task 都交给 coze 自渲染，不再强制 forest。
BINARY_SM = {"OR", "RR", "RD", "IR", "IRR", "PETO"}


def _default_plots_for(task, sm):
    """返回 task 的默认出图列表。
    - pairwise_meta：二元结局追加 labbe+trimfill；
    - 其余：直接查 DEFAULT_PLOTS，未登记返回 []（交由 coze 自渲染）。"""
    if task == "pairwise_meta":
        base = ["forest", "funnel", "baujat", "radial"]
        if (sm or "OR").upper() in BINARY_SM:
            base += ["labbe", "trimfill"]
        return base
    return list(DEFAULT_PLOTS.get(task, []))


DEFAULT_PLOTS = {
    # —— 主分析 / 配对 ——
    "pairwise_meta": ["forest", "funnel", "baujat", "radial"],  # 二元再追加 labbe+trimfill（见 _default_plots_for）
    # 以下三个 task 同处 coze 共用渲染大块（run_task.R 382-660），plots 带名即渲染，
    # 与 task 无关 → 可安全追加伴侣图（见 2026-08-28 增强）。
    "single_group_meta": ["forest", "funnel", "influence"],     # 主森林图 + 漏斗图 + 影响诊断（均引擎支持；baujat/radial 对 metaprop 不稳，不强行加）
    "subgroup_analysis": ["forest", "funnel", "baujat", "radial", "trimfill", "influence"],  # 含 by-subgroup 分层森林图 + 异质性/发表偏倚/剪补/敏感性全套诊断
    "metareg": ["forest", "funnel", "bubble"],                  # 2026-08-28 放宽 coze bubble gate 后 metareg 亦可渲染气泡图
    # —— 单图 task（1:1 映射） ——
    "forest_plot": ["forest"],
    "funnel_plot": ["funnel"],
    "labbe_plot": ["labbe"],
    "baujat_plot": ["baujat"],
    "radial_plot": ["radial"],
    "bubble_plot": ["bubble"],
    "trimfill": ["funnel"],                                      # trimfill 叠加在漏斗图上
    # —— 派生诊断 task ——
    "gosh": ["gosh"],
    "leave_one_out": ["loo"],
    "cumulative_meta": ["cumulative"],
    # 2026-08-28 修正：coze 端 run_task.R 第 574 行 `if ("influence" %in% plots)` 才出图，
    # 空 plots 仅返回 stats（诊断面板不显示）。旧值 [] 导致 influence 主图永不出现，
    # 与下方注释"coze 自动渲染影响力诊断面板"不符。改为显式 ["influence"] 方能触发出图。
    "influence": ["influence"],
    # —— NMA ——
    "nma": ["netgraph", "netleague"],
    "nma_rank": [],                                             # coze 自动渲染 SUCRA/P-score 图
    # 2026-09-14 新增：成分网络 Meta。coze 端空 plots 亦默认出 forest + netgraph，
    # 此处显式声明以对齐 coze_contract.md §3（两处口径一致，避免"契约说 default 但客户端不发"）。
    "cnma": ["forest", "netgraph"],
    # —— 其他结局 ——
    "survival_meta": ["forest", "funnel", "radial"],            # 2026-08-28 增补漏斗图 + Radial（rma 对象引擎支持）
    "diagnostic_meta": ["sroc", "sens_forest", "spec_forest"],   # 2026-08-28 增补敏感度/特异度森林图
    "bayesian_pairwise": ["forest"],                             # 2026-08-28 修复：R 端补 forest 渲染（此前空跑）
    "dose_resp": [],                                            # coze 自动渲染剂量-反应图
    "metainc": ["forest", "funnel", "radial", "influence"],     # 2026-08-28 增补漏斗/Radial/影响诊断
    "ipd_meta": ["forest", "funnel", "influence"],              # 2026-08-28 补条目并增补漏斗/影响诊断（rma.glmm 对象）
    # —— 专用分析（coze 自动主图 或 无图） ——
    "tsa": ["tsa"],                                             # 显式名（case36 实测）
    "power": ["power"],                                         # 显式名（case37 实测）
    "rob2": ["rob2"],                                           # 修正：原 rob_traffic 为旧名，coze 实际认 rob2
    "selmodel": [],                                             # coze 自动渲染选择模型图
    "rve_meta": [],                                             # coze 自动渲染稳健方差估计
    "multilevel_meta": [],
    "multivariate_meta": [],
    "nnt": [],                                                  # coze 自动渲染 NNT 图/表
    # —— 非图形（表/数值，无 plot） ——
    "esc": [],                                                  # 效应量数值转换，无图
    "prisma_flow": ["prisma_flow"],
    "prisma_checklist": [],                                     # PRISMA 检查表，无图
    "grade": [],                                                # GRADE 证据等级表，无图
}

# 已知合法 plot 名全集（用户显式 --plots 覆盖时用于过滤，避免 coze 静默丢弃未知图名）
VALID_PLOTS = frozenset({
    "forest", "funnel", "labbe", "baujat", "radial", "trimfill", "influence",
    "bubble", "netgraph", "contribution", "nodesplit", "netleague", "sucra",
    "sroc", "dose_resp", "loo", "cumulative", "drapery", "tsa", "power",
    "rob2", "gosh", "prisma_flow", "sens_forest", "spec_forest",
})


# 用户语言判定逻辑已上移至 ct-base/scripts/i18n.py（detect_text_language / _normalize_language / resolve_user_language），本文件不再重复实现。


# 列名别名表（中/英同义 → 规范键）；先吃掉大部分"列名不匹配"，减少 LLM 兜底触发
COLUMN_ALIASES = {
    "event_exp": ["event_exp", "实验组事件", "实验组事件数", "处理组事件", "干预组事件",
                  "阳性数", "事件数_exp", "e_exp", "treatment_event", "exp_event"],
    "n_exp": ["n_exp", "实验组样本量", "实验组人数", "实验组总数", "处理组样本量",
              "干预组样本量", "样本量_exp", "n_exp_total", "treatment_n", "exp_n"],
    "event_ctrl": ["event_ctrl", "对照组事件", "对照组事件数", "事件数_ctrl",
                   "e_ctrl", "control_event", "ctrl_event"],
    "n_ctrl": ["n_ctrl", "对照组样本量", "对照组人数", "对照组总数", "样本量_ctrl",
               "n_ctrl_total", "control_n", "ctrl_n"],
    "mean_exp": ["mean_exp", "实验组均数", "实验组均值", "处理组均数", "干预组均数", "m_exp"],
    "sd_exp": ["sd_exp", "实验组标准差", "实验组sd", "处理组标准差", "干预组标准差", "s_exp"],
    "mean_ctrl": ["mean_ctrl", "对照组均数", "对照组均值", "m_ctrl"],
    "sd_ctrl": ["sd_ctrl", "对照组标准差", "对照组sd", "s_ctrl"],
}


# 亚组变量列名别名表（中文标签 → 数据实际列名）。
# classify 从 query 提取的是中文标签（如"地区"），未必等于数据列名（region）；
# 本表在 build 阶段（已知真实列名）做解析，解析不出则发显式告警，
# 不再像旧版那样静默把亚组退化为空、导致 subgroup_analysis 失效。
SUBGROUP_ALIASES = {
    "地区": "region", "地域": "region", "区域": "region", "国家": "country", "洲": "region",
    "年份": "year", "发表年份": "year", "年": "year",
    "年龄": "age", "年龄段": "age", "老年": "age",
    "性别": "sex", "男女性别": "sex", "gender": "sex",
    "剂量": "dose", "给药剂量": "dose",
    "疗程": "duration", "治疗时长": "duration", "干预时长": "duration",
    "干预时间": "duration", "运动时长": "duration", "随访时长": "duration",
    "人群": "population", "种族": "race", "基线": "baseline", "严重度": "severity",
    "分期": "stage", "线数": "line",
}


# 非数值（分类）列：保持字符串透传，不参与 float 强转
NON_NUMERIC_KEYS = {"treatment"}  # nma 臂标签列

# 不消费 params.sm 的 task（写入 sm 属噪音字段且会误导用户以为能换尺度）
# - diagnostic_meta：合成灵敏度/特异度（SROC 曲线），非 OR 类效应量
# - survival_meta：固定合并 logHR→HR，HR 即尺度，sm 不参与
# 注：nma / cnma 仍消费 sm（netmeta sm 参数，二分类默认 OR / 连续型须显式 MD|SMD），不可剔除。
NON_SM_TASKS = {"diagnostic_meta", "survival_meta"}


# NMA 三种输入格式的列契约（对齐 run_task.R .nma_prep）：
#   对比二分类: treat1/treat2 + event1/n1/event2/n2
#   对比连续:   treat1/treat2 + te/sete（亦认 TE/seTE）
#   arm 二分类: treatment + event + n
#   arm 连续:   treatment + te + sete
# .build_df 仅 tolower 列名、不按 colmap 重命名 → 必须把别名归一化为下方小写 canonical 名。
NMA_FORMATS = [
    {
        "name": "contrast_binary",
        "canonical": ["treat1", "treat2", "event1", "n1", "event2", "n2"],
        "aliases": {
            "treat1": ["treat1", "处理1", "干预1", "组1", "t1"],
            "treat2": ["treat2", "处理2", "干预2", "组2", "t2"],
            "event1": ["event1", "事件1", "阳性1", "e1"],
            "n1": ["n1", "样本量1", "人数1", "总数1", "nn1"],
            "event2": ["event2", "事件2", "阳性2", "e2"],
            "n2": ["n2", "样本量2", "人数2", "总数2", "nn2"],
        },
        "non_numeric": ["treat1", "treat2"],
    },
    {
        "name": "contrast_cont",
        "canonical": ["treat1", "treat2", "te", "sete"],
        "aliases": {
            "treat1": ["treat1", "处理1", "干预1", "组1", "t1"],
            "treat2": ["treat2", "处理2", "干预2", "组2", "t2"],
            "te": ["te", "TE", "效应量", "logor", "logOR", "y"],
            "sete": ["sete", "seTE", "se", "SE", "标准误"],
        },
        "non_numeric": ["treat1", "treat2"],
    },
    {
        "name": "arm_bin",
        "canonical": ["treatment", "event", "n"],
        "aliases": {
            "treatment": ["treatment", "干预", "处理", "组", "arm", "treat"],
            "event": ["event", "事件", "阳性", "events", "evt", "e"],
            "n": ["n", "样本量", "人数", "总数", "nn", "total", "N"],
        },
        "non_numeric": ["treatment"],
    },
    {
        "name": "arm_cont",
        "canonical": ["treatment", "te", "sete"],
        "aliases": {
            "treatment": ["treatment", "干预", "处理", "组", "arm", "treat"],
            "te": ["te", "TE", "效应量", "logor", "logOR", "y"],
            "sete": ["sete", "seTE", "se", "SE", "标准误"],
        },
        "non_numeric": ["treatment"],
    },
]


def _detect_nma_format(raw_rows, override=None):
    """探测 NMA 数据格式 → (resolved{canonical:actual}, unresolved, non_numeric)。
    对比格式(treat1/treat2 命中) 优先于 arm-based；同组内 binary/cont 取「完整命中」者，
    均无完整命中则取命中列最多者交 LLM 兜底；完全识别不出 → exit 2 兜底。"""
    if not raw_rows:
        return {}, list(NMA_FORMATS[0]["canonical"]), set()
    actual_cols = list(raw_rows[0].keys())
    norm_to_actual = {_norm(c): c for c in actual_cols}
    ov = json.loads(override) if override else None

    def _match(canonical, aliases):
        if ov and canonical in ov:
            v = ov[canonical]
            if v in actual_cols or _norm(v) in norm_to_actual:
                return norm_to_actual.get(_norm(v), v)
            return None
        if canonical in actual_cols:
            return canonical
        return next((norm_to_actual[_norm(al)] for al in aliases if _norm(al) in norm_to_actual), None)

    def _try(fmt):
        resolved, unresolved = {}, []
        for k in fmt["canonical"]:
            hit = _match(k, fmt["aliases"].get(k, []))
            if hit:
                resolved[k] = hit
            else:
                unresolved.append(k)
        return resolved, unresolved, len(resolved)

    def _pick(formats, key_col):
        """在 formats 中选最优：key_col 命中 → 优先完整命中(format 全部解析)，否则命中最多者。"""
        best = None
        for fmt in formats:
            resolved, unresolved, score = _try(fmt)
            if key_col not in resolved:
                continue
            if not unresolved:
                return resolved, unresolved, set(fmt["non_numeric"])  # 完整命中直接返回
            if best is None or score > best[2]:
                best = (resolved, unresolved, score, fmt)
        if best is not None:
            return best[0], best[1], set(best[3]["non_numeric"])
        return None

    # 1) 对比格式优先（treat1/treat2 为锚）
    hit = _pick((NMA_FORMATS[0], NMA_FORMATS[1]), "treat1")
    if hit:
        return hit
    # 2) arm-based（treatment 为锚）
    hit = _pick((NMA_FORMATS[2], NMA_FORMATS[3]), "treatment")
    if hit:
        return hit
    # 3) 都识别不出 → 返回 arm_bin 的 unresolved 集，交 LLM 兜底（红线：有边界兜底，不破快路径）
    resolved, unresolved, _ = _try(NMA_FORMATS[2])
    return resolved, unresolved, set(NMA_FORMATS[2]["non_numeric"])


def _norm(s):
    return (s or "").strip().lower()


def _resolve_colmap(raw_rows, canonical_keys, override=None):
    """规范键 → 数据实际列名（精确 → 别名 → override 优先）。
    返回 (resolved{canonical:actual}, unresolved[canonical])。"""
    if not raw_rows:
        return {}, list(canonical_keys)
    actual_cols = list(raw_rows[0].keys())
    norm_to_actual = {_norm(c): c for c in actual_cols}
    resolved, unresolved = {}, []
    for key in canonical_keys:
        if override and key in override:               # LLM 兜底回灌优先
            ov = override[key]
            if ov in actual_cols or _norm(ov) in norm_to_actual:
                resolved[key] = norm_to_actual.get(_norm(ov), ov)
                continue
            unresolved.append(key)                      # override 列名不存在 → 仍交 LLM 重判
            continue
        if key in actual_cols:                          # 精确匹配
            resolved[key] = key
            continue
        hit = next((norm_to_actual[_norm(al)] for al in COLUMN_ALIASES.get(key, [])
                    if _norm(al) in norm_to_actual), None)
        if hit:                                         # 别名匹配
            resolved[key] = hit
            continue
        unresolved.append(key)
    return resolved, unresolved


def _classify_non_numeric_cols(raw_rows, extra_cols):
    """判定哪些额外列应作为字符串透传（不 float 强转）。
    逻辑：列名含 categorical/arm/臂/组/strain/type/allocation/region 等语义，
    或整列值含非数字字符（如 'BCG-Moreau'、'Open'）→ 字符串透传。
    纯数字列（如 latitude、followup_years）→ 返回数值强转。
    这是 P0-1 协变量透传的关键：分类协变量/多臂标识列不得被 float() 打爆。
    """
    non_num = set()
    for c in extra_cols:
        base = c.lower().replace("_", "").replace("-", "")
        if any(tok in base for tok in ("categorical", "stratum", "arm", "group",
                                        "strain", "type", "allocation", "alloc",
                                        "region", "country", "vaccine", "manufacturer",
                                        "route", "population", "blind")):
            non_num.add(c)
            continue
        # 抽样前几行看是否有非纯数字值
        sample = [str(r.get(c, "")) for r in raw_rows[:20] if r.get(c, "") not in (None, "")]
        if sample and not all(re.fullmatch(r"[-+]?\d*\.?\d+([eE][-+]?\d+)?", s.strip()) for s in sample):
            non_num.add(c)
    return non_num


def _resolve_subgroup(subgroup, actual_cols):
    """把 classify 提取的亚组标签（可能是中文）解析为数据真实列名。
    解析顺序：精确匹配列名 → SUBGROUP_ALIASES 中文别名 → 否则显式告警并返回 None
    （旧版此处静默返回空，导致 subgroup_analysis 退化为无分层主分析，属隐蔽错误，
     会诱发 agent 反复重试；现改为 stderr 告警，让失效可见）。"""
    if not subgroup:
        return None
    cols = set(actual_cols.keys()) if isinstance(actual_cols, dict) else set(actual_cols)
    if subgroup in cols:
        return subgroup
    canon = SUBGROUP_ALIASES.get(subgroup) or SUBGROUP_ALIASES.get(_norm(subgroup))
    if canon and canon in cols:
        return canon
    sys.stderr.write(
        f"[build_request][WARN] subgroup 列 '{subgroup}' 不在数据列 {sorted(cols)} 中，"
        "亚组分析将退化为无分层主分析。请检查列名，或用 --colmap 指定（如 subgroup 对应列）。\n"
    )
    return None


def _emit_fallback(unresolved, available, spec):
    """列解析失败时，发出结构化兜底信号（exit 2）→ 由 LLM 最小判断后回灌 --colmap 重跑。
    LLM 兜底范围严格受限：只补缺的列映射 / 纠正 measure·model，禁止重读文档、禁止重算。"""
    fb = {
        "status": "needs_llm_fallback",
        "reason": "column_unresolved",
        "unresolved_columns": unresolved,
        "available_columns": available,
        "partial_spec": spec,
        "hint": ("LLM 仅补充缺的列映射（最小判断）：用 "
                 "--colmap '{\"event_exp\":\"<实际列名>\",...}' 重跑 build_request.py；"
                 "如需纠正效应量/模型，加 --measure / --model。禁止重读 SKILL/references/adapter/config，禁止重算。"),
    }
    print(json.dumps(fb, ensure_ascii=False, indent=2))
    sys.exit(2)


def _load_rows(data_arg, data_json):
    """读取研究数据 → 统一的 JSON 行数组（list[dict]）。

    红线（用户要求 2026-08-27）：无论输入是 CSV 还是 JSON 文件，本函数一律
    归一化为 JSON 行数组；下游 build() 把该 JSON 直接塞进 coze payload，
    coze 端永远只接收 JSON，绝不接收原始 CSV 文件。
    """
    if data_json:
        obj = json.loads(data_json)
    elif data_arg:
        if data_arg.lower().endswith(".csv"):
            # ★ CSV → JSON：读成行数组（每行一个 dict），后续作为 JSON 发往 coze
            # 用 utf-8-sig 读取以剥掉 BOM——extract_assist 用 utf-8-sig 写（带 BOM），
            # 若用 utf-8 读，首列名会变成 "\ufeffstudy"，被误判为额外列且 study 值丢失。
            with open(data_arg, encoding="utf-8-sig", newline="") as f:
                obj = list(csv.DictReader(f))
        else:
            obj = json.load(open(data_arg, encoding="utf-8"))
    else:
        return None
    if isinstance(obj, dict) and "rows" in obj:
        rows = obj["rows"]
    elif isinstance(obj, list):
        rows = obj
    else:
        raise ValueError("数据须为行数组或 {'rows': [...]}")
    # ★ 强制 JSON 归一化守卫：确保可被 json.dumps 序列化（coze 端只收 JSON）
    json.dumps(rows, ensure_ascii=False)
    return rows


def _coerce_rows(rows, resolved, carry_cols=None, non_numeric=None):
    """按 resolved（canonical→actual）取值并转数值。carry_cols 为需原样透传（字符串）的额外列
    （如亚组变量列），non_numeric 为分类/标签列（如 nma 的 treatment/treat1/treat2 臂名），
    两者均不参与数值强转。空值/非数值（数值列）→ 硬错误。"""
    carry_cols = carry_cols or []
    non_numeric = non_numeric or NON_NUMERIC_KEYS
    out = []
    for i, r in enumerate(rows):
        rec = {"study": r.get("study") or str(i + 1)}
        # 协变量/额外列透传：分类/臂列字符串原样，数值协变量（latitude/followup 等）float 强转
        for c in carry_cols:
            if c not in r or r[c] in (None, ""):
                continue
            if c in non_numeric:
                rec[c] = r[c]
                continue
            try:
                rec[c] = float(r[c])
            except (TypeError, ValueError):
                rec[c] = r[c]  # 非纯数字（如缺失标记）→ 字符串透传，不阻断
        for canonical, actual in resolved.items():
            v = r.get(actual)
            if v in (None, ""):
                raise ValueError(f"数据缺列：{canonical}（实际列 {actual} 为空）")
            if canonical in non_numeric:
                rec[canonical] = v
                continue
            try:
                rec[canonical] = float(v)
            except (TypeError, ValueError):
                raise ValueError(f"数据列 {canonical}（实际列 {actual}）值非数值：{v!r}")
        out.append(rec)
    return out


def build(query=None, spec=None, data_arg=None, data_json=None, out_path="request.json",
          colmap_override=None, measure_override=None, model_override=None,
          language_override=None):
    spec = spec or _classify(query or "")
    if spec.get("track") == "topic":
        raise SystemExit("[build_request] 选题轨不走计算路径；请用 literature_probe.py（见 §2.2）")

    raw_rows = _load_rows(data_arg, data_json)
    # 显式记录：若原始输入是 CSV，已转换为 JSON 行数组再发 coze（用户要求 2026-08-27）
    if raw_rows and data_arg and data_arg.lower().endswith(".csv"):
        sys.stderr.write(
            f"[build_request] 输入为 CSV，已转换为 JSON（{len(raw_rows)} 行）后发往 coze；"
            "coze 端只接收 JSON。\n"
        )
    if not raw_rows:
        # 无数据且 classify 判定缺字段 → 报错并列出缺的列
        if spec.get("needs_clarify"):
            raise SystemExit("[build_request] 缺字段：" + "; ".join(spec.get("missing_fields", [])))
        raise SystemExit("[build_request] 未提供研究数据（--data / --data-json）")
    # 数据已随 --data 提供时，覆盖 classify 仅凭 query 文本判定的 needs_clarify
    # （classify 看不到 --data 文件内容，避免误报缺字段）
    spec["needs_clarify"] = False
    spec["missing_fields"] = []

    # —— 列解析：精确 → 别名 → （override 优先）→ 仍缺则发 LLM 兜底信号 ——
    override = json.loads(colmap_override) if colmap_override else None
    if spec.get("task") == "nma":
        # NMA 三种输入格式自动探测（对比二分类/对比连续/arm 二分类/arm 连续），
        # 不盲信 classify 固定的 arm-based 列模板（见 coze_contract.md §3 / run_task.R .nma_prep）。
        resolved, unresolved, non_numeric = _detect_nma_format(raw_rows, colmap_override)
        carry_cols = []
        subgroup = None
    else:
        spec_colmap = spec.get("colmap") or []
        resolved, unresolved = _resolve_colmap(raw_rows, spec_colmap, override)
        # 亚组变量列不在 colmap 内，必须原样透传（否则 coze 收不到该列、subgroup_analysis 静默失效）
        subgroup = (spec.get("params_extra") or {}).get("subgroup")
        # 解析亚组列名（中文标签→真实列名）；解析不出发显式告警并退化为无分层，不再静默失效
        subgroup = _resolve_subgroup(subgroup, raw_rows[0] if raw_rows else {})
        # ★ 协变量透传（P0-1 修复，BCG 案例打脸）：除核心结局列 + subgroup 外，
        #   CSV 中的「额外列」全部原样透传（如 latitude/allocation/vaccine_type 等协变量、
        #   arm 多臂标识），供 coze 端做元回归/亚组分析。数值协变量 float 强转，
        #   分类/臂标识列字符串透传（靠 _coerce_rows 的 NON_NUMERIC_KEYS 判断）。
        resolved_keys = set(resolved)
        extra_cols = [c for c in (raw_rows[0].keys() if raw_rows else [])
                      if c != "study" and c not in resolved_keys and c != (subgroup or "")]
        carry_cols = [subgroup] if subgroup else []
        carry_cols += extra_cols
        # 分类协变量/臂标识列：凡含 latin/categorical 语义或值非纯数字 → 字符串透传
        non_numeric = set(NON_NUMERIC_KEYS) | _classify_non_numeric_cols(raw_rows, extra_cols)
    if unresolved:
        available = list(raw_rows[0].keys()) if raw_rows else []
        _emit_fallback(unresolved, available, spec)
    try:
        rows = _coerce_rows(raw_rows, resolved, carry_cols, non_numeric)
    except ValueError as e:
        raise SystemExit("[build_request] " + str(e))

    model_key = model_override or spec.get("model") or "REM-L"
    coze_model, common, random = MODEL_MAP.get(model_key, MODEL_MAP["REM-L"])

    params = {
        "model": coze_model,
        "common": common,
        "random": random,
    }
    # 用户语言备用字段（注入 coze 入参 params）：coze 可据其决定报告/图表文案语言。
    # 判定优先级：① 显式 --language 最高；② 否则按【输入 query 文本内容】判定
    #   （中文系统 + 英文输入 → en，而非被系统 locale 误判 zh）；③ query 为空时
    #   回退到系统 locale（i18n._current_lang）。属"备用"输入，不强制覆盖 coze 自身判定。
    # 复用 ct-base i18n.resolve_user_language：三级优先级（显式 > 内容级文本 > 系统 locale）
    if ctbase_i18n is not None:
        params["user_language"] = ctbase_i18n.resolve_user_language(
            query if query else "", language_override
        )
    else:
        params["user_language"] = "en"  # ct-base 缺失退化兜底（正常不应触发）
    # sm（效应量尺度）仅对消费 sm 的 task 写入。diagnostic_meta / survival_meta 不消费 sm，
    # 写 OR 属噪音字段且会误导用户以为可换尺度 → 跳过（见 coze_contract.md §3）。
    if spec.get("task") not in NON_SM_TASKS:
        params["sm"] = measure_override or spec.get("measure") or "OR"
    if subgroup:
        params["subgroup"] = subgroup

    task = spec.get("task") or "pairwise_meta"
    default_plots = _default_plots_for(task, params.get("sm"))
    user_plots = (spec.get("params_extra") or {}).get("plots")
    if user_plots:
        # 用户指定的图与任务默认图取并集（不替换默认）：森林图等必备图始终保留，
        # 避免用户 query 提"漏斗图"反而挤掉森林图（classify 把图名当显式 plots 时尤其易发）。
        merged = set(default_plots)
        merged.update(p for p in user_plots if p in VALID_PLOTS)
        plots = list(merged)
    else:                                            # 默认：按 task 取 coze_contract §3 默认 plots
        plots = default_plots

    req = {
        "task": task,
        "data": {"rows": rows, "colmap": {k: k for k in resolved}},
        "params": params,
        "figure": {"plots": plots},
        # 调用方约束（2026-08-30）：产物直接可 POST /run（带有效归因，空归因会绕过限流）。
        "query_origin": _origin(),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(req, f, ensure_ascii=False, indent=2)
    return req


def main():
    ap = argparse.ArgumentParser(description="meta-analysis 计算轨 request.json 装配（零 LLM、零计算）")
    ap.add_argument("--query", help="用户原始请求（内部调 classify）")
    ap.add_argument("--spec", help="预生成 classify 输出 JSON")
    ap.add_argument("--data", help="研究数据文件（.csv / .json）")
    ap.add_argument("--data-json", help="研究数据内联 JSON（行数组 / {'rows':[...]}）")
    ap.add_argument("--out", default="request.json", help="输出 request.json 路径")
    ap.add_argument("--colmap", help="LLM 兜底回灌：列映射 JSON，{规范键:实际列名}，如 '{\"event_exp\":\"实验组事件数\"}'")
    ap.add_argument("--measure", help="LLM 兜底回灌：效应量覆盖（OR/RR/RD/MD/SMD/HR…）")
    ap.add_argument("--model", help="LLM 兜底回灌：模型覆盖（REM-L/MH）")
    ap.add_argument("--language", help="用户语言（zh/en/...），覆盖自动检测，注入 coze 入参 user_language 备用")
    a = ap.parse_args()

    spec = None
    if a.spec:
        spec = json.load(open(a.spec, encoding="utf-8"))
    req = build(query=a.query, spec=spec, data_arg=a.data, data_json=a.data_json, out_path=a.out,
                colmap_override=a.colmap, measure_override=a.measure, model_override=a.model,
                language_override=a.language)
    print(json.dumps(req, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
