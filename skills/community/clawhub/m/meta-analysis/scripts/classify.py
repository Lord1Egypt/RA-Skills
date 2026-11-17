#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classify.py — meta-analysis 技能的双轨路由 / 归一化脚本

设计目标（对齐 §0 双轨门控 + 延迟不变量）：
  - 零 LLM 决策：确定性关键词表映射，LLM 不纠结"该用哪个 task / measure"。
  - 零计算：仅做字符串匹配 + 拼 JSON，绝不跑 R / Python 算任何统计量。
  - 零出网：纯本地字符串处理。
  - 对应 ct-advisor 的 scripts/route.py（一次 code 判定，LLM 不决策路由），
    但比 route.py 多输出结构化 spec，可直接喂 run_analysis.py 的 request.json。

输入：用户原始 query 字符串（命令行参数）
输出：spec JSON（stdout）
  {
    "track": "compute" | "topic",
    "task": "pairwise_meta" | "subgroup_analysis" | "metareg" | "nma" | "cnma" | "survival_meta"
          | "diagnostic_meta" | "ipd_meta"
          | "prisma_flow" | "prisma_checklist" | "rob2" | "rob_summary" | "grade",
    "measure": "OR" | "RR" | "RD" | "MD" | "SMD" | "HR" | null,
    "model": "REM-L" | "MH",
    "data_type": "binary" | "continuous" | "diagnostic" | "survival" | "ipd" | null,
    "params_extra": {"plots": [...], "subgroup": "...", "tool": "ROB2|ROB1|ROBINS-I"},
    "needs_clarify": bool,
    "missing_fields": [str],
    "colmap": [列名建议]
  }

task 语义分两类（2026-08-30 划分，决定第 7 步的缺参判定）：
  - 效应量类（pairwise_meta / ... / ipd_meta）：需要研究数据（event/n 或效应量+SE）。
  - 综述流程类（prisma_flow / prisma_checklist / rob2 / rob_summary / grade）：
    不需要效应量数据，各自契约见 REVIEW_TASK_MISSING；误用 has_data 判据会把
    「对这12项研究做偏倚风险评价」这类句子放行（句含数字）→ 静默返回答非所问的
    合并效应量，属最危险的一类误路由：不报错、给错答案。
"""
import sys
import json
import re
import argparse


# ---- 关键词表（语言中立，不翻译）----
TOPIC_WORDS = [
    "选题", "方向", "可行性", "没方向", "没思路", "选课题", "确定课题",
    "no topic", "which topic", "decide a topic", "choose a topic",
    "feasibility", "candidate", "topic",
]
BINARY_WORDS = ["二分类", "binary", "事件", "event", "发生率", "发生数", "阳性", "反应", "risk"]
CONT_WORDS = ["连续", "continuous", "均数", "mean", "均差", "smd", "mean diff"]
DIAG_WORDS = ["诊断", "diagnostic", "sroc"]
SURV_WORDS = ["生存", "survival", "survival meta"]
IPD_WORDS = ["个体", "ipd", "raw data", "个体数据"]
HR_WORDS = ["hr", "hazard", "风险比"]          # 风险比 → 生存 HR
OR_WORDS = ["or", "odds ratio", "比值比"]
RR_WORDS = ["rr", "risk ratio", "相对危险度", "relativerisk"]
RD_WORDS = ["rd", "risk difference", "危险差"]
MD_WORDS = ["md", "mean diff", "均数差"]
SMD_WORDS = ["smd", "标准化均数差", "standardized mean difference"]
REML_WORDS = ["随机效应", "reml", "random", "异质性", "随机"]
MH_WORDS = ["固定效应", "fixed", "mh", "mantel", "固定"]
SUBGROUP_WORDS = ["亚组", "subgroup", "分层"]
METAREG_WORDS = ["元回归", "metareg", "meta regression", "回归分析"]
NMA_WORDS = ["网络", "network", "nma", "网状"]
# 成分网络 Meta（CNMA）关键词（2026-09-14 新增）。
# ⚠️ 判定必须**前置**于 NMA_WORDS：CNMA 问句通常同时含「网络」（如"成分网络 meta"），
#    顺序颠倒会被 NMA 抢走 → 落到普通 arm-based NMA，与用户意图不符。
#    注意 "cnma" 字符串内含 "nma"，同样依赖前置顺序。
CNMA_WORDS = ["成分网络", "成分 meta", "成分meta", "cnma", "component network",
              "component nma", "组分网络", "ingredient-level", "成分-效应", "成分效应"]
FUNNEL_WORDS = ["漏斗", "funnel"]
EGGER_WORDS = ["发表偏倚", "egger", "begg", "pub bias", "publication bias"]

# ---- 综述流程类关键词（2026-08-30 新增）----
# 背景：run_task.R 早已注册 prisma_flow / prisma_checklist / rob2 / grade / ipd_meta，
#   但 classify 长期只认 6 个效应量 task，综述类一个不认 → 相关请求 100% 落到
#   pairwise_meta，再被第 7 步要求「提供研究数据」（对综述类完全是错的指引）。
# 判定顺序按「具体到宽泛」排：GRADE 必须在 ROB 之前（「证据质量评价」同时含
#   GRADE 的「证据质量」与 ROB 的「质量评价」），否则会被 ROB 抢走。
PRISMA_FLOW_WORDS = ["prisma流程图", "prisma 流程图", "prisma flow", "prisma图", "prisma 图",
                     "flow diagram", "流程图", "四阶段图", "文献筛选图"]
PRISMA_CHECKLIST_WORDS = ["prisma检查表", "prisma 检查表", "prisma checklist", "checklist",
                          "检查表", "报告清单", "27项", "prisma 2020"]
GRADE_WORDS = ["grade", "证据分级", "证据质量", "证据等级", "证据确信度", "certainty of evidence"]
ROB_WORDS = ["偏倚风险", "风险偏倚", "risk of bias", "rob2", "rob 2", "robins", "robvis",
             "质量评价", "质量评估", "方法学质量", "文献质量"]
IPD_META_WORDS = ["ipd meta", "ipd", "个体数据meta", "个体患者数据", "individual patient data"]

# RoB 判断矩阵的迹象词：命中说明用户已给出各研究的 judgement，可直接出图；
# 未命中则应引导先产出 Study + D1..D5 判断表，而不是拿去跑效应量合并。
ROB_JUDGEMENT_WORDS = ["低风险", "高风险", "中风险", "有一定顾虑", "不清楚", "low risk",
                       "high risk", "some concerns", "unclear", "critical",
                       "评价结果", "已评价", "judgement", "judgment"]

# 综述流程类 task（数据契约与效应量 Meta 完全不同，走独立缺参判定）
REVIEW_TASKS = {"prisma_flow", "prisma_checklist", "rob2", "rob_summary", "grade"}

# 各综述 task 缺参时给用户的正确指引（替换掉对它们毫无意义的「study data」）
REVIEW_TASK_MISSING = {
    "prisma_flow": ["PRISMA counts: records / duplicates / screened / excluded_title / "
                    "assessed / excluded_elig / included (numbers)"],
    "rob2": ["RoB judgement table: one row per study, columns Study + D1..D5 "
             "(Low / Some concerns / High)"],
    "rob_summary": ["RoB judgement table: one row per study, columns Study + D1..D5 "
                    "(Low / Some concerns / High)"],
}

# 默认列模板（data_type → 列名建议），供 agent 套用归一化
COLMAP = {
    "binary": ["event_exp", "n_exp", "event_ctrl", "n_ctrl"],
    "continuous": ["mean_exp", "sd_exp", "n_exp", "mean_ctrl", "sd_ctrl", "n_ctrl"],
    "diagnostic": ["tp", "fp", "fn", "tn"],
    "survival": ["n_event_exp", "time_exp", "n_event_ctrl", "time_ctrl"],
    "nma": ["treatment", "event", "n"],  # classify 默认提示=arm-based 二分类；连续/对比格式由 build_request._detect_nma_format 按数据列名自动探测（见 [2.2.11]）
    "ipd": ["study", "group", "outcome"],
}


def _hit(text, words):
    t = text.lower()
    return any(w.lower() in t for w in words)


def _extract_subgroup(text):
    # 匹配「按 X / by X / 分层 X / subgroup X」，X 为亚组列名（中文或英文，1-8 字符）。
    # 用前瞻在动词/标点处断词，避免贪心吞掉「做亚组分析」等后续词
    # （旧版 {1,6} 无边界，会把「按地区做亚组分析」截成「地区做亚组分」，
    #  导致下游别名表接不住、亚组静默失效）。
    # 修复：列名字符类必须含数字 0-9 —— pdl1 / ki67 / egfr / her2 等带数字的亚组列
    # 原 [A-Za-z_\u4e00-\u9fa5] 不含数字，导致整列无法被捕获，subgroup 退化为 None、
    # build_request 静默退化为无分层主分析（隐蔽错误，会诱使 agent 反复重试）。
    # 同时 (?:...)(?:\s+by)? 吃掉「subgroup by X」里多余的 by，避免把 by 误当成列名。
    pat = re.compile(
        r'(?:按|by|分层|subgroup)(?:\s+by)?\s*([A-Za-z0-9_\u4e00-\u9fa5]{1,8}?)'
        r'(?=做|进|行|分|析|亚组|分层|的|\(|\)|（|）|，|,|\s|$|。|；|;)',
        re.IGNORECASE,
    )
    m = pat.search(text)
    if not m:
        return None
    return m.group(1) or None


def _has_prisma_counts(text):
    """是否提供了 PRISMA 筛选计数（句中含有数字）。

    必须先剔除「PRISMA 2020」这类**版本短语**里的数字——它是最常见的说法
    （「画一张 PRISMA 2020 流程图」），若直接判 `re.search(r'\\d', q)` 会把 2020
    当成筛选计数，于是带着全 0 参数放行，coze 端静默出一张空流程图。
    """
    t = re.sub(r"prisma\s*20\d{2}", "prisma", text, flags=re.IGNORECASE)
    return bool(re.search(r"\d", t))


def classify(query):
    q = query or ""

    # 1) track（选题词优先级最高）
    track = "topic" if _hit(q, TOPIC_WORDS) else "compute"

    # 2) task（覆盖默认 pairwise_meta）
    #    综述流程类必须**前置**于效应量类：run_task.R 早已实现，但 classify 长期不认，
    #    且此类问句常自带数字（「对这12项研究做偏倚风险评价」），若走效应量分支会被
    #    第 7 步的 has_data 判据放行，直接提交 coze 拿到答非所问的合并效应量。
    if _hit(q, PRISMA_FLOW_WORDS):
        task = "prisma_flow"
    elif _hit(q, PRISMA_CHECKLIST_WORDS):
        task = "prisma_checklist"
    elif _hit(q, GRADE_WORDS):
        task = "grade"
    elif _hit(q, ROB_WORDS):
        task = "rob2"
    elif _hit(q, IPD_META_WORDS):
        task = "ipd_meta"
    elif _hit(q, CNMA_WORDS):
        task = "cnma"
    elif _hit(q, NMA_WORDS):
        task = "nma"
    elif _hit(q, SUBGROUP_WORDS):
        task = "subgroup_analysis"
    elif _hit(q, METAREG_WORDS):
        task = "metareg"
    elif _hit(q, SURV_WORDS) or _hit(q, HR_WORDS):
        task = "survival_meta"
    elif _hit(q, DIAG_WORDS):
        task = "diagnostic_meta"
    else:
        task = "pairwise_meta"

    # 3) data_type
    if task == "diagnostic_meta":
        data_type = "diagnostic"
    elif task in ("nma", "cnma"):
        # cnma 与 nma 共用数据契约（治疗标签 + 事件/样本量，标签以 sep_comps 拼接成分，
        # 如 "A+B"）——列模板与格式探测完全一致，见 build_request._detect_nma_format
        data_type = "nma"
    elif task == "survival_meta":
        data_type = "survival"
    elif task == "ipd_meta":
        data_type = "ipd"
    elif task in REVIEW_TASKS:
        # 综述流程类没有「效应量数据类型」的概念；置 None 可让 agent 不去套 colmap
        data_type = None
    elif _hit(q, CONT_WORDS):
        data_type = "continuous"
    elif _hit(q, BINARY_WORDS):
        data_type = "binary"
    elif _hit(q, IPD_WORDS):
        data_type = "ipd"
    else:
        data_type = "binary"  # 默认二分类（最常见）

    # 4) measure
    if task in REVIEW_TASKS:
        # 综述流程类：效应量 / 合并模型 / 异质性估计全不适用，显式置空
        measure = None
    elif task == "survival_meta" or _hit(q, HR_WORDS):
        measure = "HR"
    elif _hit(q, OR_WORDS):
        measure = "OR"
    elif _hit(q, RR_WORDS):
        measure = "RR"
    elif _hit(q, RD_WORDS):
        measure = "RD"
    elif _hit(q, SMD_WORDS):
        measure = "SMD"
    elif _hit(q, MD_WORDS):
        measure = "MD"
    else:
        measure = "OR" if data_type == "binary" else ("SMD" if data_type == "continuous" else None)

    # 5) model（默认随机效应 REML）
    model = None if task in REVIEW_TASKS else ("MH" if _hit(q, MH_WORDS) else "REM-L")

    # 6) plots / subgroup var / RoB tool（不改 task）
    params_extra = {}
    plots = []
    if task not in REVIEW_TASKS:
        # 漏斗图 / Egger 只对效应量 Meta 有意义；综述类带上会让 coze 端 plots 参数失真
        if _hit(q, FUNNEL_WORDS):
            plots.append("funnel")
        if _hit(q, EGGER_WORDS):
            plots.append("egger")
    if task in ("rob2", "rob_summary"):
        # plot_rob_traffic / plot_rob_summary 的 tool 映射：ROB2(5域) / ROB1(6域) / ROBINS-I(7域)
        if _hit(q, ["robins", "robins-i"]):
            tool = "ROBINS-I"
        elif _hit(q, ["rob1", "cochrane", "考克兰"]):
            tool = "ROB1"
        else:
            tool = "ROB2"
        params_extra["tool"] = tool
    subgroup = _extract_subgroup(q) if task == "subgroup_analysis" else None
    if plots:
        params_extra["plots"] = plots
    if subgroup:
        params_extra["subgroup"] = subgroup

    # 7) 数据迹象校验（仅 compute 轨需要）
    has_data = bool(re.search(r'\d+\s*/\s*\d+', q)) or (
        _hit(q, ["研究", "数据", "事件", "样本", "effect", "or=", "rr=", "hr=", "md=", "se="])
        and re.search(r'\d', q)
    )
    # 综述流程类不能套用 has_data（它是「是否给了效应量数据」的判据）：
    #   「对这12项研究做偏倚风险评价」句含数字 + 「研究」→ has_data=True → 旧逻辑放行，
    #   提交 coze 后 .build_df 拿到的是空/错误结构，静默返回答非所问的合并效应量。
    #   故对 REVIEW_TASKS 走各自的契约判定。
    needs_clarify = False
    missing_fields = []
    if track == "compute":
        if task in REVIEW_TASKS:
            if task == "prisma_flow" and not _has_prisma_counts(q):
                # 筛选计数必然含数字；一句数字都没有就是没给计数
                # （用 _has_prisma_counts 而非裸 \d，以排除「PRISMA 2020」的版本号）
                needs_clarify = True
                missing_fields = list(REVIEW_TASK_MISSING["prisma_flow"])
            elif task in ("rob2", "rob_summary") and not _hit(q, ROB_JUDGEMENT_WORDS):
                # 未出现任何 judgement 取值词 → 先引导产出判断表，别拿去跑合并
                needs_clarify = True
                missing_fields = list(REVIEW_TASK_MISSING["rob2"])
            # prisma_checklist / grade：纯 params，全默认即可运行，不拦
        elif not has_data:
            needs_clarify = True
            missing_fields = ["study data (event/n per arm, or effect size + SE)"]

    if track == "topic":
        # 选题轨：task/measure/model/data_type/colmap 无意义，置空避免误导 agent
        task = measure = model = data_type = None
        colmap = []
        params_extra = {}

    return {
        "track": track,
        "task": task,
        "measure": measure,
        "model": model,
        "data_type": data_type,
        "params_extra": params_extra,
        "needs_clarify": needs_clarify,
        "missing_fields": missing_fields,
        "colmap": COLMAP.get(data_type, []),
    }


def main():
    ap = argparse.ArgumentParser(description="meta-analysis 双轨路由/归一化（零 LLM、零计算）")
    ap.add_argument("query", help="用户原始请求字符串")
    args = ap.parse_args()
    spec = classify(args.query)
    print(json.dumps(spec, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
