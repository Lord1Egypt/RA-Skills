# Diagnostic Test Meta-Analysis / 诊断准确性Meta分析

> **优先调用封装** / Prefer the wrapper: `source("src/r_engine/advanced_functions.R")` →
> `run_diagnostic_meta(data, cols=list(TP="TP",FP="FP",FN="FN",TN="TN"))` + `plot_sroc(fit)`。
> 以下为底层 `mada` API 说明，供需要精细控制时参考。

## reitsma() — Bivariate Model / 双变量模型（推荐）

> Reitsma (2005) bivariate random-effects model — the standard for diagnostic
> test accuracy (pooled sensitivity, specificity, SROC). / 诊断准确性 Meta 的标准方法。

```r
library(mada)

# Data must contain columns: TP, FP, FN, TN (one row per study)
fit <- reitsma(df)         # 双变量随机效应模型
summary(fit)               # pooled sens/spec, AUC, correlation

# SROC curve with study points + summary point + confidence/prediction region
plot(fit, sroclwd = 2,
     main = "SROC — Bivariate (Reitsma) Model")
points(fpr(df), sens(df), pch = 1)     # 各研究散点
legend("bottomright", c("Study", "Summary"), pch = c(1, 19))
```

### Descriptive stats / 描述性统计

```r
madad(df)                  # per-study sens/spec + 95% CI, DOR, LR+, LR-
```

### Summary points & likelihood ratios / 汇总点与似然比

```r
SummaryPts(fit)            # pooled sens, spec, LR+, LR-, DOR (with CI)
```

## Model comparison / 模型对照

| Purpose | Function (mada) | Notes |
|---------|-----------------|-------|
| Bivariate summary (推荐) | `reitsma(df)` | 汇总 sens/spec + 相关性 + SROC |
| Descriptive per-study | `madad(df)` | 各研究 sens/spec/DOR/LR ± CI |
| Summary points / LR | `SummaryPts(fit)` | 从拟合对象提取汇总指标 |
| Univariate DOR | `madauni(df)` | 单变量 DOR（较少用） |

> ⚠️ 常见误用：`mada::phm()` 是"比例风险"式模型，**不接受** `precursor` / `model="ds"` 等参数；
> 诊断 Meta 的标准入口是 `reitsma()`。封装 `run_diagnostic_meta()` 已固定为正确调用。

---

## Data Format / 数据格式

| Required | Description |
|----------|-------------|
| study | Study identifier (可选，用于标注) |
| TP | True positives |
| FP | False positives |
| FN | False negatives |
| TN | True negatives |

---

## Output Measures / 输出指标

- Sensitivity (Sens) = TP / (TP + FN)
- Specificity (Spec) = TN / (TN + FP)
- DOR (Diagnostic Odds Ratio) = (TP/FN) / (FP/TN)
- LR+ = Sens / (1-Spec)
- LR- = (1-Sens) / Spec
- AUC(SROC) = area under summary ROC curve

---

## References / 引用
- Doebler P, Holling H. (2015). mada: Meta-analysis of diagnostic accuracy. R package.
- Reitsma JB, et al. (2005). Bivariate analysis of sensitivity and specificity produces informative summary measures in diagnostic reviews. *J Clin Epidemiol*, 58(10), 982-990.
- Rutter CM, Gatsonis CA. (2001). A hierarchical regression approach to meta-analysis of diagnostic test accuracy evaluations. *Stat Med*, 20(19), 2865-2884.
