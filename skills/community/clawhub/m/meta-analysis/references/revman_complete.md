# RevMan Feature 100% Mapping Table

## RevMan 5.x → R Code Mapping

本文件列出 RevMan 5.x 中所有可用功能及其对应的 R 实现代码。用户在 RevMan 中熟悉的操作均可通过 R 精确复现。

---

## I. Review Creation & Data Management

### 1.1 New RevMan Review → Initialize Data Frame

```r
# RevMan: File → New Review
# R 对应:
meta_data <- data.frame(
  study = character(),
  year = integer(),
  event_exp = integer(),
  n_exp = integer(),
  event_ctrl = integer(),
  n_ctrl = integer(),
  stringsAsFactors = FALSE
)
```

### 1.2 Add Comparison → Define Analysis Structure

```r
# RevMan: Add Comparison
meta_data <- rbind(meta_data, data.frame(...))
```

### 1.3 Add Outcome → Define Analysis Variables

```r
# RevMan: Add Outcome → Dichotomous/Continuous
outcome_type <- "Dichotomous"  # 或 "Continuous"
```

### 1.4 Input Study Data → Build Data Frame

```r
# RevMan: Input study data
# R 对应:
meta_data <- data.frame(
  study = c("Smith2020", "Jones2019", "Lee2021"),
  event_exp = c(15, 20, 12),
  n_exp = c(100, 95, 80),
  event_ctrl = c(30, 35, 28),
  n_ctrl = c(100, 90, 78)
)
```

---

## II. Analysis Type Selection

### 2.1 Dichotomous Data

```r
# RevMan: Analysis → Dichotomous
library(meta)

# 法 1: Mantel-Haenszel
mh_result <- metabin(
  event.e = event_exp,
  n.e = n_exp,
  event.c = event_ctrl,
  n.c = n_ctrl,
  studlab = study,
  data = meta_data,
  method = "MH",
  sm = "OR",           # "OR", "RR", "RD"
  combined.figures = TRUE,
  combined.events = FALSE
)

# 法 2: Peto 法（罕见事件）
peto_result <- metapeto(
  event.e = event_exp,
  n.e = n_exp,
  event.c = event_ctrl,
  n.c = n_ctrl,
  studlab = study,
  data = meta_data,
  sm = "OR"
)
```

### 2.2 Continuous Data

```r
# RevMan: Analysis → Continuous
cont_result <- metacont(
  n.e = n_exp,
  mean.e = mean_exp,
  sd.e = sd_exp,
  n.c = n_ctrl,
  mean.c = mean_ctrl,
  sd.c = sd_ctrl,
  studlab = study,
  data = meta_data,
  sm = "SMD",          # "SMD", "MD"
  method.mean = "Luo",  # 均值计算方法
  method.sd = "Shi"     # SD 计算方法
)
```

### 2.3 O-E and Variance（O-E/V）

```r
# RevMan: Analysis → O-E and Variance
# 适用于已计算效应量的情况
oe_result <- metagen(
  TE = yi,
  seTE = sqrt(vi),
  studlab = study,
  data = effect_size_data,
  sm = "GENQ"
)
```

### 2.4 Generic Inverse Variance

```r
# RevMan: Analysis → Generic Inverse Variance
# 直接输入效应量 + 标准误
giv_result <- metagen(
  TE = logOR,
  seTE = se,
  studlab = study,
  data = effect_size_data
)
```

---

## III. Effect Size Pooling Models

### 3.1 Fixed Effect Model

```r
# RevMan: Analysis → Fixed Effect
fe_result <- metabin(
  data = meta_data,
  method = "MH",
  sm = "OR",
  method.tau = "FE"      # RevMan 固定效应
)

# metafor 对应
fe_rma <- rma(yi = yi, vi = vi, method = "FE", data = effect_data)
```

### 3.2 Random Effects Model

```r
# RevMan: Analysis → Random Effects → DerSimonian-Laird
dl_result <- metabin(
  data = meta_data,
  method = "MH",
  sm = "OR",
  method.tau = "DL"      # DerSimonian-Laird
)

# RevMan: Analysis → Random-effects model → Restricted Maximum Likelihood (REML)
reml_rma <- rma(yi = yi, vi = vi, method = "REML", data = effect_data)
```

---

## IV. Forest Plot

### 4.1 RevMan Default Forest Plot

```r
# RevMan: Forest Plot 右侧面板
# R 对应:
library(meta)
forest(mh_result)
```

### 4.2 Custom Forest Plot (Add Columns)

```r
# RevMan: Custom columns in forest plot
forest(mh_result,
  leftcols = c("studlab", "event.e", "n.e", "event.c", "n.c"),
  rightcols = c("effect", "ci", "w.random"),
  colgap.studlab = "3%",
  fs.heading = 10,
  ff.heading = "B"
)
```

### 4.3 RevMan Style → ggplot Style

```r
# RevMan 风格（类似 RevMan 5 的黑白方块风格）
library(ggplot2)

# 使用 forestploter（出版级森林图，替代 ggforestplot；CRAN 可用、R4.6 适配）
library(forestploter)
# 构造 CI 文本列（forestploter 按列布局，支持多列 CI）
effect_data$`HR (95% CI)` <- sprintf("%.2f (%.2f-%.2f)",
  exp(effect_data$logOR),
  exp(effect_data$logOR - 1.96 * effect_data$se),
  exp(effect_data$logOR + 1.96 * effect_data$se))
p <- forest(effect_data,
  est = logOR,
  lower = logOR - 1.96 * effect_data$se,
  upper = logOR + 1.96 * effect_data$se,
  ci_column = "HR (95% CI)",
  ref_line = 0,
  xlab = "log(OR)",
  theme = theme_forest()
)
plot(p)
```

---

## V. Funnel Plot

### 5.1 RevMan Default Funnel Plot

```r
# RevMan: Funnel plot icon
# R 对应:
funnel(mh_result)
```

### 5.2 Add Contour Lines

```r
# Revman: Funnel plot with contour lines
funnel(mh_result, contour = c(0.9, 0.95, 0.99))
```

### 5.3 Custom Funnel Plot

```r
funnel(mh_result,
  yaxis = "invvar",
  xlim = c(-3, 3),
  ylim = c(0, 1),
  refline = 0,
  col = "darkblue"
)
```

---

## VI. Heterogeneity

### 6.1 RevMan Heterogeneity Output

```r
# RevMan 自动输出: I², tau², Q, df, p-value
# R 对应:
cat(sprintf("I² = %.1f%%\n", mh_result$I2 * 100))
cat(sprintf("tau² = %.3f\n", mh_result$tau2))
cat(sprintf("Q = %.3f, df = %d, p = %.4f\n",
  mh_result$Q, mh_result$df.Q, mh_result$pval.Q))
```

### 6.2 Prediction Interval

```r
# RevMan: 仅在 metafor 中可用
predict_int <- predict(reml_rma)
cat(sprintf("Prediction Interval: [%.3f, %.3f]\n",
  predict_int$pred - 1.96*sqrt(predict_int$se^2 + reml_rma$tau2),
  predict_int$pred + 1.96*sqrt(predict_int$se^2 + reml_rma$tau2)))
```

---

## VII. Subgroup Analysis

### 7.1 RevMan Subgroup Accumulating Forest Plot

```r
# Revman: Subgroup → Add subgroup
# R 对应:
metabias_result <- update.meta(mh_result,
  byvar = factor(subgroup_group),
  bylab = "Subgroup",
  print.byvar = FALSE,
  comb.fixed = FALSE,
  comb.random = TRUE,
  byseparator = " ==> "
)
```

### 7.2 Meta-Analysis Subgroup Test (metafor)

```r
# 更精确的亚组分析
library(metafor)

subgroup_rma <- rma(yi = yi, vi = vi,
  mods = ~ factor(group) - 1,   # 无截距模型
  data = effect_data
)

# 组间异质性检验
subgroup_wald <- anova(subgroup_rma, btt = 2:length(unique(group)))
```

---

## VIII. Sensitivity Analysis

### 8.1 Leave-One-Out

```r
# Revman: Sensitivity → Leave one out
# R 对应:
library(metafor)
leave1out_results <- leave1out(reml_rma)
print(leave1out_results)
```

### 8.2 Filter by Quality

```r
# Revman: Sensitivity → High quality only
high_quality_data <- meta_data[meta_data$rob_score >= 6, ]
hq_result <- metabin(data = high_quality_data, ...)
```

### 8.3 L'Abbé Plot

```r
# Revman: 用于比例数据的散点图
labbe(mh_result)
```

---

## IX. Publication Bias

### 9.1 RevMan Bias Risk Test

```r
# Revman: Tests for funnel plot asymmetry → Egger/Begg
# R 对应:
metabias(mh_result, method = "egger")
metabias(mh_result, method = "begg")
```

### 9.2 Trim and Fill

```r
# Revman: Performance → Trim-and-Fill
# R 对应:
tf_result <- trimfill(mh_result)
forest(tf_result)
```

---

## X. GRADE Evidence Quality Assessment

```r
# Revman: GRADEpro assessment criteria
# R 对应——结构化评估框架:

assess_grade_evidence <- function(analysis_result, risk_of_bias,
  inconsistency, indirectness, imprecision, publication_bias) {
  
  # 起始质量: 观察性研究 = 低, RCT = 高质量
  
  grade_score <- data.frame(
    domain = c("Risk of Bias", "Inconsistency", "Indirectness",
               "Imprecision", "Other considerations"),
    assessment = c(risk_of_bias, inconsistency, indirectness,
                   imprecision, publication_bias),
    downgrade = c(-1, -1, -1, -1, -1)  # 各问题降级
  )
  
  return(grade_score)
}
```

---

## XI. Network Meta-Analysis

### 11.1 Create Network Structure

```r
# Revman: Network Meta-Analysis (NMA)
# R 对应:
library(netmeta)

# 数据格式: study, treat1, treat2, TE, seTE
nma_result <- netmeta(
  TE = logOR,
  seTE = se,
  treat1 = treatment,
  treat2 = comparator,
  studlab = study,
  data = nma_data,
  sm = "OR",
  level = 0.95
)
```

### 11.2 League Table

```r
# Revman: League table
league_table <- netleague(nma_result)
league_table$random
league_table$fixed
```

### 11.3 Intervention Ranking

```r
# Revman: 干预效果排序
rank_result <- netrank(nma_result, small.values = "bad")
print(rank_result)
plot(rank_results)
```

---

## XII. RevMan File Export

### 12.1 Export to RevMan 5 File

```r
# Revman: File → Export → RevMan 5 file
# R 概念对应（需要手动构建）:

# 保存为 CSV 供 RevMan 导入
write.csv(meta_data, "revman_export.csv", row.names = FALSE)

# 保存为通用 RDS 格式（不依赖任何外部包）
saveRDS(list(
  comparison = "Intervention vs Control",
  outcome = "Primary Outcome",
  analysis = mh_result
), "meta_analysis_results.rds")
```

---

## Key Differences

| 特性 | RevMan | R (本技能) |
|------|--------|-----------|
| **交互** | 点击菜单 | 自然语言 + R 代码 |
| **灵活性** | 受限 | 无限定制 |
| **可复现性** | 需手动记录 | 代码保存 |
| **图形** | 静态位图 | 矢量可编辑 |
| **高级方法** | 不完整 | 全覆盖 |
| **批量处理** | 不可以 | 脚本自动化 |
| **版本控制** | 不支持 | 完整 R Markdown |
