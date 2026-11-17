# API Reference / 接口参考

> 本文件集中收录技能的复用接口（强制调用规则 + 函数清单 + 示例）。运行任何分析都必须 `source()` 对应脚本并调用下列函数，禁止从零编写完整分析脚本。

## Reusable API / 复用接口（强制）

> **规则：任何分析必须调用已有函数，禁止从零编写完整分析脚本。**
> When running any analysis, ALWAYS `source()` the skill scripts and call the functions below — never rewrite the full pipeline inline.

### 基础 API / Core API

```r
# 统一入口：效应量计算 + 模型拟合，返回 ma_result 对象
source("src/r_engine/meta_analysis_core.R")
res <- ma_analyze(data, type = "rate",            # binary|continuous|rate|precomp|survival
                                               # |correlation|single_proportion|single_mean
                  measure = "IRR",                # 自动选 OR/SMD/IRR/ZCOR/PLOGIT(PLO)/MN 等
                  method = "REML", test = "knha")

# 一行出图 + 摘要（森林图/漏斗图 SVG+PNG + results.md）
ma_save(res, outdir = "output", prefix = "meta")
```

Functions: `ma_analyze()`(分发) · `calculate_effect_size()` · `run_meta_analysis()` · `analyze_heterogeneity()` · `analyze_publication_bias()` · `run_subgroup_analysis()` · `run_meta_regression()` · `run_sensitivity_analysis()` · `create_forest_plot()` · `create_funnel_plot()` · `generate_results_summary()` · `ma_save()`.
Column names are case-insensitive; override mapping via `cols = list(a="A", b="B", c="C", d="D")`.

**Forest 5 themes**: `create_forest_plot(res, style = "revman")` — `style ∈ {revman, classic, modern, lancet, nejm}`（配色/菱形形状随主题切换）。

### 高级诊断与可视化封装 / Advanced Diagnostics

```r
# 高级诊断/可视化封装：GOSH / Baujat / Drapery / Power / Bayesian pairwise / 诊断Meta / RoB
source("src/r_engine/advanced_functions.R")

g  <- run_gosh(res$model); plot_gosh(g)          # GOSH 敏感性(子集拟合密度散点)
plot_baujat(res$model, top_n = 5)                # Baujat 异质性-影响力图(top_n 高亮标签)
plot_drapery(es_data, labels, type = "zvalue")   # Drapery 置信曲线(meta::drapery)
pw <- run_power_curve(effect = 0.3, k_range = 2:30, i2 = 0.5)   # 功效曲线(自实现,无依赖) -> $k_needed
bp <- run_bayes_pairwise(es_data, labels, tau_prior = "halfnormal")  # bayesmeta 两组贝叶斯
dx <- run_diagnostic_meta(data, cols = list(TP="TP",FP="FP",FN="FN",TN="TN")); plot_sroc(dx)  # mada::reitsma 双变量 SROC
plot_rob_traffic(rob_data, tool = "ROB2"); plot_rob_summary(rob_data)  # robvis 红绿灯/汇总图
```

Advanced functions: `run_gosh()` · `plot_gosh()` · `plot_baujat()` · `plot_drapery()` · `run_power_curve()` · `run_bayes_pairwise()` · `run_diagnostic_meta()` · `plot_sroc()` · `plot_rob_traffic()` · `plot_rob_summary()`.
缺依赖时自动给出友好安装提示（bayesmeta / mada / robvis / ggrepel）。

## 重依赖封装函数 / Heavy-Dependency Wrappers

```r
# TSA 试验序贯分析：自实现，无需外部包（连续型 d / 二分类 or）
ts <- run_tsa(es_data, labels, effect_type = "continuous", d = 0.3)   # -> $RIS $cum_Z $crossed $plot

# 剂量-反应：dosresmeta。shape 控制模型形状(线/曲)；binary 的 study_design 指研究设计(cc/ci/ir)
dr1 <- run_dose_resp(yi="y", dose="dose", id="id", data=ari,
                     outcome="continuous", shape="linear", sd="sd", n="n")          # 连续型(smd)
dr2 <- run_dose_resp(yi="logrr", dose="dose", id="id", data=alcohol_cvd,
                     outcome="binary", shape="quadratic",
                     se="se", cases="cases", n="n", study_design="type")            # 二分类(gl)

# 生存 Meta（run_surv_meta 现已本地用 metafor 逆方差合并 logHR）；贝叶斯 NMA 用 gemtc(JAGS)，multinma 为可选后端
sm <- run_surv_meta(yi="loghr", vi="v", studlab="study", data=hr_df, method="REML")
bn <- run_bayes_nma_multinma(prep, priors)     # multinma (Stan, 可选后端)
bg <- run_bayes_nma_gemtc(data.ab, treatments, studies)   # gemtc (JAGS)
```

Batch-2 functions: `run_tsa()` · `run_dose_resp()` · `run_surv_meta()` · `run_bayes_nma_multinma()` · `run_bayes_nma_gemtc()`.
⚠️ `run_tsa()`/`run_dose_resp()` 沙盒内已实跑验证；`run_surv_meta()` 现已本地实跑（metafor）；`run_bayes_nma_gemtc()` 需本机装 JAGS、`run_bayes_nma_multinma()` 需本机装 Stan 工具链，封装做友好提示，请在**本机**运行。
📌 无 `meta::tes()`（`meta` 包不存在该函数，历史文档有误）；TSA 一律用自实现的 `run_tsa()`。
