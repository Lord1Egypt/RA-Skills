# Advanced Analysis Methods / 高级分析方法

## 目录 / Table of Contents

1. [多水平元分析 (Multilevel Meta-Analysis)](#1-多水平元分析)
2. [多元元分析 (Multivariate Meta-Analysis)](#2-多元元分析)
3. [IPD 元分析 (Individual Patient Data)](#3-ipd-元分析)
4. [贝叶斯网状 Meta 分析](#4-贝叶斯网状-meta-分析)
5. [元分析中的因果推断](#5-元分析中的因果推断)
6. [剂量反应 Meta 分析](#6-剂量反应-meta-分析)
7. [罕见事件 Meta 分析](#7-罕见事件-meta-分析)
8. [预测区间与 prognostic](#8-预测区间)

---

## 1. Multilevel Meta-Analysis / 多水平元分析

**适用于**：同一研究报告多个结局、多组比较、或研究间存在聚类结构。

### 1.1 Three-Level Model / 三水平模型

```r
library(metafor)

# Level 1: 抽样方差
# Level 2: 研究内（多结局/多组）
# Level 3: 研究间

mlma_result <- rma.mv(
  yi = yi,
  V = vi,
  random = list(~ 1 | study_id, ~ 1 | outcome_id),
  data = mlma_data,
  method = "REML"
)

# 输出方差成分
print(mlma_result)

# 跨层异方差
mlma_het <- rma.mv(
  yi = yi,
  V = diag(tau2_within) + diag(tau2_between),
  random = list(~ 1 | study_id, ~ 1 | outcome_id),
  data = mlma_data,
  method = "REML",
  control = list(optimizer = "optim")
)
```

### 1.2 Multi-Arm Study Handling / 多臂研究处理

```r
# 多臂研究（Bolding et al. 处理方法）
# 需要构建方差-协方差矩阵

library(metafor)

# 构建 covariances 矩阵 for multi-arm studies
# CS 结构（复合对称）
V_matrix <- lapply(unique(mlma_data$study_id), function(s) {
  sub <- mlma_data[mlma_data$study_id == s, ]
  k <- nrow(sub)
  vi <- sub$vi
  tau2 <- mlma_result$sigma2[1]
  
  V <- matrix(tau2, nrow = k, ncol = k)
  diag(V) <- vi
  V
})

# 运行多水平模型
library(clubSandwich)
mlma_result <- rma.mv(
  yi = yi,
  V = V_matrix,
  random = ~ 1 | study_id/outcome_id,
  data = mlma_data,
  method = "REML"
)
```

---

## 2. Multivariate Meta-Analysis / 多元元分析

**适用于**：同时分析多个相关结局（如血压的收缩压和舒张压）。

```r
library(metafor)

# 准备数据：需要多个结局 per study
# study_id, outcome_type, yi, vi

mvma_result <- rma.mv(
  yi = yi,
  V = vi_matrix,
  random = ~ outcome_type | study_id,
  struct = "UN",  # 非结构化协方差
  data = mvma_data,
  method = "REML"
)

# 提取研究间方差成分
sigma <- mvma_result$sigma2
cat("Between-study variance for outcome 1:", sigma[1], "\n")
cat("Between-study variance for outcome 2:", sigma[2], "\n")
cat("Between-study covariance:", mvma_result$rho * prod(sqrt(sigma)), "\n")

# 模型比较
mvma_CS <- rma.mv(yi, vi_matrix, random = ~ outcome_type | study_id,
  struct = "CS", data = mvma_data)
mvma_UN <- rma.mv(yi, vi_matrix, random = ~ outcome_type | study_id,
  struct = "UN", data = mvma_data)

anova(mvma_CS, mvma_UN)  # 检验结构选择
```

---

## 3. IPD Meta-Analysis / IPD 元分析

**适用于**：获得原始个体参与者数据（最理想情况）。

```r
library(ipdmeta)

# IPD 格式: study_id, patient_id, treatment, outcome, covariates
# 两步法

# Step 1: 每项研究拟合 IPD 模型
ipd_within <- lapply(unique(ipd$study_id), function(s) {
  sub <- ipd[ipd$study_id == s, ]
  glm(outcome ~ treatment + age + sex, data = sub, family = binomial)
})

# Step 2: 汇总各研究效应
effect_estimates <- sapply(ipd_within, function(m) coef(m)["treatment"])
standard_errors <- sapply(ipd_within, function(m) summary(m)$coefficients["treatment", "Std. Error"])

# 合并
two_step_result <- metagen(
  TE = effect_estimates,
  seTE = standard_errors,
  sm = "OR"
)

# 一步法（混合效应模型）
one_step_result <- glm(
  outcome ~ treatment + age + sex + factor(study_id) + treatment:study_id,
  data = ipd,
  family = binomial
)
```

---

## 4. Bayesian Network Meta-Analysis / 贝叶斯网状 Meta 分析

**适用于**：≥3 种干预需要排序，考虑先验信息。

```r
library(gemtc)
library(rjags)

# 准备数据
# study, treatment, responders, sampleSize（二分类）
# 或 study, treatment, mean, sd, sampleSize（连续型）

# 创建 network 对象
network <- mtc.network(
  data.ab = gemtc_data,
  description = "Network meta-analysis",
  treatments = treatments_list
)

# 构建一致性模型
model <- mtc.model(
  network,
  type = "consistency",
  linearModel = "random",
  n.chain = 4,
  likelihood = "binom",
  link = "logit"
)

# 运行 MCMC
results <- mtc.run(model, n.adapt = 5000, n.iter = 20000, thin = 10)

# 一致性检验: 节点拆分
split <- mtc.nodesplit(network, linearModel = "random")

# 结果
results  # 联赛表
forest(results)

# SUCRA（Surface Under Cumulative Ranking）
rank_probs <- rank.probability(results)
sucra <- cumrank(rank_probs)

# 收敛诊断
gelman.diag(results)
plot(results)  # 后验密度图
```

### 4.1 Advanced Bayesian NMA / 贝叶斯 NMA 进阶

```r
# 加入协变量调整
network$studies$duration <- c(8, 12, 24, 16)  # 研究持续时间

# 回归调整
model_adjusted <- mtc.model(
  network,
  type = "regression",
  regressor = list(
    coefficient = "shared",
    coefficient = "off",
    "duration"
  ),
  linearModel = "random"
)
```

---

## 5. Causal Inference in Meta-Analysis / 元分析中的因果推断

**适用于**：目标 trial emulation（在观察性研究 meta 中模拟 RCT）。

```r
library(metafor)
library(WeightIt)

# 计算逆方差权重
ipd_data$propensity <- glm(treatment ~ cov1 + cov2 + cov3,
  data = ipd_data, family = binomial)$fitted

ipd_data$iptw <- ifelse(ipd_data$treatment == 1,
  1 / ipd_data$propensity,
  1 / (1 - ipd_data$propensity))

# 加权元分析
weighted_rma <- rma(
  yi = yi,
  vi = vi,
  weights = iptw,
  data = ipd_data,
  method = "REML"
)
```

---

## 6. Dose-Response Meta-Analysis (dosresmeta run_dose_resp) / 剂量反应 Meta 分析（dosresmeta 封装 run_dose_resp）

**适用于**：评估暴露剂量与疾病风险的（线性/曲线）关系。

> ✅ **优先调用封装** `run_dose_resp()`（在 `advanced_functions.R`）。它已固化两处关键区分与
> 易错点，避免手写 dosresmeta 时踩坑：
> 1. **模型形状**（线性/二次曲线）由 `shape` 控制并写入 formula —— **不要**用 `type` 或
>    虚构的 `degree` 参数来控制形状（dosresmeta 无 `degree`）。
> 2. dosresmeta 的 `type` 参数**专指二分类的“研究设计”**（`cc`=病例对照 / `ci`=累积发病 /
>    `ir`=发病率），经 `study_design` 传入（列名或统一字符串）。
> 3. 协方差近似 `covariance` 合法值：`gl / h / md / smd / user / indep`（**无 "ho"**）。
>    缺省：二分类 `gl`，连续型 `smd`。

```r
source("src/r_engine/advanced_functions.R")

# ---- 二分类结局（logRR/logOR + cases + n + 研究设计 type）----
data(alcohol_cvd)   # cols: id/author/type/dose/cases/n/logrr/se
dr_lin <- run_dose_resp(
  yi = "logrr", dose = "dose", id = "id", data = alcohol_cvd,
  outcome = "binary", shape = "linear",
  se = "se", cases = "cases", n = "n",
  study_design = "type"        # 列名，值为 cc/ci
)                              # -> gl 协方差近似

dr_quad <- run_dose_resp(       # 二次曲线：logrr ~ dose + I(dose^2)
  yi = "logrr", dose = "dose", id = "id", data = alcohol_cvd,
  outcome = "binary", shape = "quadratic",
  se = "se", cases = "cases", n = "n", study_design = "type"
)

# ---- 连续型结局（均数 + sd + n）----
data(ari)                       # cols: id/author/dose/y/sd/n
dr_cont <- run_dose_resp(
  yi = "y", dose = "dose", id = "id", data = ari,
  outcome = "continuous", shape = "linear",
  sd = "sd", n = "n"           # -> smd 协方差近似
)

# 返回 list(fit, plot)；plot 为剂量-反应曲线(含 95%CI 带)，参照点取最小剂量
summary(dr_lin$fit)
if (!is.null(dr_lin$plot)) print(dr_lin$plot)
```

---

## 7. 罕见事件 Meta-Analysis / 罕见事件Meta分析

**适用**：多项研究零事件时传统方法偏倚。

```r
# 7.1 Peto 法（仅 OR，一阶近似）
peto_or <- metabin(
  event.e = event_exp,
  n.e = n_exp,
  event.c = event_ctrl,
  n.c = n_ctrl,
  studlab = study,
  data = meta_data,
  sm = "OR",
  method = "Peto"
)

# 7.2 Mantel-Haenszel + 连续性校正
mh_or_corrected <- update(
  peto_or,
  method = "MH",
  incr = 0.5  # Haldane 校正
)

# 7.3 贝叶斯方法（推荐用于零事件）
library(bayesmeta)

bayes_zero <- bayesmeta(
  y = yi,
  sigma = sqrt(vi),
  labels = study,
  mu.prior = c(mean = 0, sd = 2),  # 保守先验
  tau.prior = function(t) dhalfnormal(t, scale = 1)
)
```

---

## 8. Prediction Interval / 预测区间

```r
# 预测区间 — 衡量新研究可能落入的范围
library(metafor)

result <- rma(yi, vi, data = effect_data, method = "REML")

pred_lower <- result$beta[1] - qt(0.975, df = k - 2) *
  sqrt(result$tau2 + result$se^2)

pred_upper <- result$beta[1] + qt(0.975, df = k - 2) *
  sqrt(result$tau2 + result$se^2)

cat(sprintf("95%% CI: [%.3f, %.3f]\n", result$ci.lb, result$ci.ub))
cat(sprintf("95%% PI: [%.3f, %.3f]\n", pred_lower, pred_upper))

# 可视化: 森林图加预测区间
forest(result,
  addpred = TRUE,
  header = TRUE,
  xlab = "Log Odds Ratio",
  slab = study_names,
  alim = c(-3, 3),
  steps = 5,
  psize = 1,
  efac = 1,
  col = "#0072B2"
)
```

---

## 9. Model Diagnostics in Meta-Analysis / 元分析中的模型诊断

```r
# 影响分析
influence_result <- influence(result)
print(influence_result)
plot(influence_result)

# 标准化 residuals
rstandard(result)

# Cook's distance
cooks.distance(result)

# DFFITS 准则
dffits(result)

# 影响力森林图（仅保留 influential studies 高亮）
forest(result,
  subset = !cooks.d > 4/length(yi),
  col = c("#E69F00", "#0072B2")[as.numeric(cooks.d > 4/length(yi)) + 1]
)
```

---

## 10. Sample Size Planning & Power Analysis / 样本量规划与功效分析

> **优先调用封装** / Prefer the wrapper: `source("src/r_engine/advanced_functions.R")` →
> `run_power_curve()`。该函数**自实现无外部依赖**（Valentine/Borenstein 功效公式，
> 含固定效应与随机效应 I² 校正双曲线），返回 `$data` / `$plot` / `$k_needed` / `$v_study`，
> 比 `metapower` / `dmetar` 更稳健（避免包缺失/API 变动）。

```r
source("src/r_engine/advanced_functions.R")

# 功效曲线: 固定研究间样本量，研究数 k 从 2 到 30 时功效如何变化
pc <- run_power_curve(
  effect       = 0.3,     # 预期效应量 (d)
  n1 = 50, n2 = 50,       # 每研究两组样本量
  k_range      = 2:30,    # 研究数扫描范围
  i2           = 0.5,     # 异质性 (0–1)
  measure      = "d",
  sig_level    = 0.05,
  target_power = 0.80
)

pc$k_needed          # 达到 80% 功效所需的最少研究数（随机效应，含 I²）
print(pc$plot)       # ggplot 功效曲线（固定 vs 随机双线 + 目标功效参考线）
ggsave("power_curve.png", pc$plot, width = 8, height = 5, dpi = 300)
```

### 备选：metapower::mpower()（如需其可视化）

```r
library(metapower)   # 若缺失，请手动安装 metapower 包

# 注意真实 API 参数名（非 power_d，此函数不存在）
mp <- mpower(
  effect_size = 0.3,   # 预期效应量
  study_size  = 100,   # 每研究总样本量 (n1+n2)
  k           = 15,    # 研究数量
  i2          = 0.5,   # 异质性
  es_type     = "d"    # d | or | r
)
print(mp)            # mp$power 观测功效; plot_mpower(mp) 出图
```
