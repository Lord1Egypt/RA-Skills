# Stata → R Meta-Analysis Command Mapping

## metareg (Stata) → rma + permutest (R)

### Feature Comparison

| Stata metareg 特性 | R 等价实现 | 说明 |
|---------------------|-----------|------|
| `metareg logor year, wsse(se) permute(1000)` | `run_metareg_R(yi, vi, ~ year, data, permute=TRUE, nperm=1000)` | 核心元回归 + permutation test |
| `metareg logor year quality, wsse(se)` | `run_metareg_R(yi, vi, ~ year + quality, data)` | 多变量元回归 |
| `metareg logor, wsse(se) cumulative` | `run_cumulative_metareg(yi, vi, ~ 1, data, sort_by="year")` | 累积元回归 |
| `metareg logor year, wsse(se) graph` | `run_metareg_R(..., plot=TRUE)` | Bubble plot |
| Knapp-Hartung 检验 | `test = "knha"` | 默认启用 |
| REML 估计 | `method = "REML"` | 默认 |
| ML 估计 | `method = "ML"` | 可选 |

### Full Example

**Stata**:
```stata
use meta_data, clear
metareg logor year, wsse(se) permute(1000) graph
metareg logor year quality_score, wsse(se) permute(5000)
metareg logor, wsse(se) cumulative graph
```

**R（本技能）**:
```r
source("src/r_engine/stata_equivalents.R")

# 基础元回归 + permutation
run_metareg_R(yi = logor, vi = se^2, mods = ~ year,
              data = meta_data, permute = TRUE, nperm = 1000)

# 累积元回归
run_cumulative_metareg(yi = logor, vi = se^2, mods = ~ 1,
                        data = meta_data, sort_by = "year")
```

---

## mvmeta (Stata) → rma.mv (R)

### Feature Comparison

| Stata mvmeta 特性 | R 等价实现 | 说明 |
|---------------------|-----------|------|
| `mvmeta lb se, study(study) outcome(outcome) bs(un)` | `run_mvmeta_R(yi, V, study_id, outcome_type, struct = "UN")` | 非结构化协方差 |
| `mvmeta lb se, study(study) outcome(outcome) bs(cs)` | `run_mvmeta_R(yi, V, study_id, outcome_type, struct = "CS")` | 复合对称 |
| `mvmeta lb se, study(study) outcome(outcome) bs(hcs)` | `run_mvmeta_R(..., struct = "HCS")` | 异质CS |
| `mvmeta lb se, study(study) outcome(outcome) bs(ar1)` | `run_mvmeta_R(..., struct = "AR1")` | 一阶自回归 |
| `mvmeta lb se, study(study) id(study) bs(un)` | `run_mvmeta_R(..., struct = "FE")` | 固定效应 |
| `mvmeta lb se, wdisplay(Q)` | `run_Q_test_mvmeta(fit)` | Cochran Q 检验 |
| 模型比较 (LR Test) | `run_lrtest_mvmeta(fit1, fit2)` | 嵌套模型比较 |

### Full Example

**Stata**:
```stata
reshape wide lb se, i(study) j(outcome) string
mvmeta lb se, study(study) outcome(outcome) bs(un) permute(1000)
mvmeta lb se, study(study) outcome(outcome) bs(cs)
lrtest
```

**R（本技能）**:
```r
source("src/r_engine/stata_equivalents.R")

# 准备 V 矩阵（多臂研究）
V_list <- build_V_matrix_CS(study_id = data$study,
                              yi = data$yi, vi = data$vi)

# 拟合 UN 结构
fit_UN <- run_mvmeta_R(yi = data$yi, V = V_list,
                        study_id = data$study,
                        outcome_type = data$outcome,
                        struct = "UN")

# 拟合 CS 结构
fit_CS <- run_mvmeta_R(yi = data$yi, V = V_list,
                        study_id = data$study,
                        outcome_type = data$outcome,
                        struct = "CS")

# LR Test
run_lrtest_mvmeta(fit_UN, fit_CS)

# Q 检验
run_Q_test_mvmeta(fit_UN)

# 多元森林图
plot_mvmeta_forest(fit_UN, data, study = "study_id_col",
                    outcome = "outcome_type_col")
```

---

## Other Stata Commands' R Equivalents

| Stata 命令 | R 等价 | 说明 |
|-----------|--------|------|
| `metan` | `metafor::rma()` / `meta::metabin()` | 标准 meta 分析 |
| `metabias` | `metafor::regtest()` / `metafor::trimfill()` | 发表偏倚 |
| `metafunnel` | `metafor::funnel()` | 漏斗图 |
| `cumul` (Stata) (累积 meta) | `cumul` (meta) / `cumul.meta()` | 累积 meta |
| `metan` (Labbe plot) | `metafor::labbe()` | Labbe 图 |
| `ipdmetan` (IPD) | `ipdmeta` 包 | IPD meta |
| `metrim` (Trim-and-Fill) | `metafor::trimfill()` | 剪补法 |
| `mvmeta` (multi-arm) | `netmeta` 包 / `rma.mv` | 多臂 meta |

---

## Permutation Test Correspondence (Stata-Specific → R Equivalent)

Stata 的 `metareg` 默认使用 permutation test，R 的 `metafor` 使用渐近检验。
本技能通过 `permutest()` 函数实现完全等价：

```r
fit <- rma(yi, vi, mods = ~ year, data = data, method = "REML")
rnd <- permutest(fit, iter = 1000, progbar = TRUE)

# 比较渐近 vs permutation p 值
cat(sprintf("Asymptotic p = %.4f\n", fit$pval))
cat(sprintf("Permutation p = %.4f\n", rnd$pval))
```
