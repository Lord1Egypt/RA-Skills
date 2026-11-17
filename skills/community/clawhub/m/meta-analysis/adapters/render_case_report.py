# -*- coding: utf-8 -*-
"""用本地 R 引擎镜像（coze 代码同源）重跑 B1，并把结果渲染为单文件 HTML 报告。

不依赖 coze 云：直接调 coze_client.run_stage_local（→ run_task.R）。
产出的 HTML 含内联 SVG 森林图/漏斗图 + 合并效应统计卡 + 可复现 R 代码。
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import coze_client as cc
import rendering

CASE_PATH = os.path.join(HERE, "..", "cases", "case_studies.json")
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

# 2) 与信封核对：指数化合并效应
if isinstance(stats, dict):
    pooled = stats.get("pooled") or {}
    est = pooled.get("estimate")
    lo = pooled.get("ci_low")
    hi = pooled.get("ci_high")
    p = pooled.get("p")
    print("== 核对 B1 合并效应（coze 形状 stats）==")
    print("  model   :", stats.get("model"))
    print("  k       :", stats.get("k"))
    print("  logOR   : %.4f  CI[%.4f, %.4f]  p=%.4g" % (est, lo, hi, p))
    print("  OR(exp) : %.4f  CI[%.4f, %.4f]" % (
        pooled.get("estimate_exp"), pooled.get("ci_low_exp"), pooled.get("ci_high_exp")))
    het = stats.get("heterogeneity") or {}
    print("  I2      :", het.get("I2"), " tau2:", het.get("tau2"), " Q:", het.get("Q"), " Q_p:", het.get("Q_p"))
    qg = stats.get("quality_gate")
    print("  quality_gate:", json.dumps(qg, ensure_ascii=False) if qg else None)
print("  figures :", [(f.get("type"), (len(f.get("svg") or ""))) for f in figures])
print("  repro   : %d 字符" % (len(repro or "")))

# 3) 组装 render_html_report 入参并固化 HTML
out = {
    "task": result.get("task") or "pairwise_meta",
    "stats": stats,
    "figures": figures,
    # run_task.R 的 repro 已是 {r, r_version, packages} 结构，直接透传；
    # 若无则降级为空字符串兜底（render_html_report 接受 {"r": "..."}）
    "repro": repro if isinstance(repro, dict) else {"r": repro or ""},
    # 注意：不设置 _coze_endpoint_notice —— 其内置横幅文案为"回退到备用 coze 端点"，
    # 与本地 R 引擎镜像场景不符，避免误导归因。本地引擎来源已在案例文件中说明。
}

CASES_DIR = os.path.abspath(os.path.join(HERE, "..", "cases"))
os.makedirs(CASES_DIR, exist_ok=True)
html_path = rendering.render_html_report(
    out, out_dir=CASES_DIR,
    titles=["森林图 · OR（随机效应 REML）", "漏斗图 · 发表偏倚检测"],
    locale="zh",
)
if not html_path:
    print("ERROR: render_html_report 返回 None（无内容可渲染）")
    sys.exit(1)
print("\n== 报告已生成 ==")
print("  ", html_path)
print("  大小: %.1f KB" % (os.path.getsize(html_path) / 1024))
