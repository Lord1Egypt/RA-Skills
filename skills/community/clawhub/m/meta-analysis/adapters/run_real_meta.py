# -*- coding: utf-8 -*-
"""用本地 R 引擎镜像（coze 代码同源）跑真实文献数据集（case_studies_real.json）的
pairwise meta 分析，并渲染为单文件 HTML 报告。

与 render_case_report.py 的区别：数据源为真实检索抓取的四格表（EMPA-REG /
DECLARE-TIMI 58 / VERTIS-CV），而非演示用的虚构 6 篇。计算仍走本地 R 引擎
（run_task.R，coze 代码同源），不经 coze 云（开发期冻结）。
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import coze_client as cc
import rendering

CASE_PATH = os.path.join(HERE, "..", "cases", "case_studies_real.json")
CASE = json.load(open(CASE_PATH, encoding="utf-8"))
STUDIES = CASE["studies"]
EM = CASE.get("effect_measure", "OR")

# 1) 离线真实 R 计算（coze 镜像，不经 coze 云）
env = {"task": "pairwise_meta", "data": STUDIES, "params": {"effect_measure": EM}}
resp = cc.run_stage_local(env)
result = (resp.get("stage_result") or {}).get("result") or {}
stats = result.get("stats")
figures = result.get("figures") or []
repro = result.get("repro")

# 2) 与原始文献 HR 做一致性核对
print("== 真实数据 B1 合并效应（本地 R 引擎，coze 形状 stats）==")
print("  研究数 k :", len(STUDIES))
if isinstance(stats, dict):
    pooled = stats.get("pooled") or {}
    est = pooled.get("estimate")
    lo = pooled.get("ci_low")
    hi = pooled.get("ci_high")
    p = pooled.get("p")
    print("  model   :", stats.get("model"))
    print("  logOR   : %.4f  CI[%.4f, %.4f]  p=%.4g" % (est, lo, hi, p))
    print("  OR(exp) : %.4f  CI[%.4f, %.4f]" % (
        pooled.get("estimate_exp"), pooled.get("ci_low_exp"), pooled.get("ci_high_exp")))
    het = stats.get("heterogeneity") or {}
    print("  I2      :", het.get("I2"), " tau2:", het.get("tau2"), " Q:", het.get("Q"), " Q_p:", het.get("Q_p"))
print("  figures :", [(f.get("type"), len(f.get("svg") or "")) for f in figures])
print("  repro   : %d 字符" % (len(repro or "")))

# 3) 组装 render_html_report 入参并固化 HTML
out = {
    "task": result.get("task") or "pairwise_meta",
    "stats": stats,
    "figures": figures,
    "repro": repro if isinstance(repro, dict) else {"r": repro or ""},
}

CASES_DIR = os.path.abspath(os.path.join(HERE, "..", "cases"))
os.makedirs(CASES_DIR, exist_ok=True)
html_path = rendering.render_html_report(
    out, out_dir=CASES_DIR,
    titles=["森林图 · OR（随机效应 REML）· 真实文献 3 篇 CVOT", "漏斗图 · 发表偏倚检测"],
    locale="zh",
)
if not html_path:
    print("ERROR: render_html_report 返回 None（无内容可渲染）")
    sys.exit(1)
print("\n== 报告已生成 ==")
print("  ", html_path)
print("  大小: %.1f KB" % (os.path.getsize(html_path) / 1024))
