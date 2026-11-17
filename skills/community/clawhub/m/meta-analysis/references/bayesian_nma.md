# Bayesian NMA (Network Meta-Analysis) / 贝叶斯网状Meta分析

> two major backends: **gemtc (JAGS, 主后端)** and **multinma (Stan, 可选后端)**. Both handle consistency/inconsistency modeling.

> ⚠️ **环境限制**：gemtc 需 JAGS（系统程序，需本机预装）、multinma 需 Stan（cmdstanr/rstan 工具链），
> **均需外部编译**。封装 `run_bayes_nma_gemtc()` / `run_bayes_nma_multinma()` 在对应后端未安装时给出
> **友好提示**（multinma 缺失时引导改用 gemtc / netmeta），请在**本机**装好 JAGS/Stan 后运行。
>
> ✅ **优先调用封装**（在 `advanced_functions.R`），参数默认值已按官方文档固化：
> ```r
> source("src/r_engine/advanced_functions.R")
> bn <- run_bayes_nma_multinma(prep, priors, response = "events", distribution = "binomial")
> bg <- run_bayes_nma_gemtc(data.ab, treatments, studies, type = "consistency",
>                           link = "logit", likelihood = "binomial", linearModel = "random")
> ```

---

## multinma — Stan Backend (可选后端) / Stan后端（可选）

```r
library(multinma)

# Prepare data
prep <- treatment_class(treatment ~ study, data = nma_data)

# Prior specification
priors <- prior_normal(0, 2, parameter = "d") +  # treatment effect
          prior_halfnormal(0.5, parameter = "sd")   # heterogeneity

# Model fit
fit <- nma(
  prep,
  response = "events",
  n = "n",
  study = "study",
  treatment = "treatment",
  distribution = "binomial",
  priors = priors,          # 仅此一处，勿再传 prior=（重复会报错）
  chains = 4,
  iter = 4000,
  seed = 123
)

# Diagnostics
plot(fit)  # traceplots
summary(fit)
```

### Survival NMA (non-PH) / 生存数据NMA（非比例风险）

```r
fit_surv <- nma(
  prep,
  response = "time",
  n = "n",
  study = "study",
  treatment = "treatment",
  survival = "weibull",   # weibull | gamma | lognormal | loglogistic | gengamma |pexp
  prior = priors,
  chains = 4,
  iter = 6000
)

# Plot survival curves
plot(fit_surv, outcome = "survival")
```

### ML-NMR Population Adjustment / 人群校正

> ⚠️ multinma **无** `nlme_nma()` 函数（历史文档误写）。ML-NMR 人群校正仍用 `nma()`，
> 通过 `regression = ~ 协变量交互` 指定，并需先用 `add_integration()` 对总体协变量做数值积分。

```r
# 1) 对聚合数据的效应修饰协变量做积分点（IPD 研究可跳过）
prep <- add_integration(prep, covariate = distr(qnorm, mean = age_mean, sd = age_sd))

# 2) 用 nma() + regression 拟合 ML-NMR（非 nlme_nma）
fit_mlnmr <- nma(
  prep,
  regression = ~ (treatment):covariate,   # 处理-协变量交互（效应修饰）
  response = "events", n = "n",
  study = "study", treatment = "treatment",
  distribution = "binomial",
  priors = priors,
  chains = 4, iter = 4000
)
```

---

## gemtc — JAGS Backend / JAGS后端

```r
library(gemtc)

# Build network
net <- mtc.network(
  data.ab = nma_data,   # arm-level data
  treatments = treatment_levels,
  studies = study_levels
)

# Define model
model <- mtc.model(
  network = net,
  type = "consistency",    # consistency | inconsistency | regression
  link = "logit",          # logit | cloglog | identity | tdistribution
  likelihood = "binomial", # binomial | normal | poisson | clnegativebin | survival
  linearModel = "random",  # random | fixed
  om.scale = 2.5,
  dic = TRUE
)

# MCMC run
results <- mtc.run(
  model,
  n.adapt = 5000,
  n.iter = 50000,
  thin = 10
)

# Diagnostics
plot(results)
 Gelman.diag(results)
 summary(results)

# Node-split for consistency
ns <- nodesplit(net, model, results)
summary(ns)
plot(ns)
```

---

## Network Comparison / 网络结果

### League Table (Both Packages) / 联赛表（两包通用）
```r
# multinma
league <- league_table(fit)
print(league, digits = 2)

# gemtc
league <- relative.effect(results, t1 = "placebo")
```

### SUCRA / P-scores / 排序
```r
# multinma
rank(fit, "SUCRA")
# P-scores: rank(fit, "P-score")

# gemtc
rank.probability(results, preferredDirection = -1)
```

---

## Diagnostics / 诊断

| Check | multinma | gemtc |
|-------|----------|-------|
| Convergence | R-hat, n_eff, traceplots | Gelman.digraph, traceplots |
| Inconsistency | `devdev()` node-splitting | `nodesplit()` |
| Model fit | LOOIC, WAIC | DIC |
| Funnel | `ggplot(study-specific)` | `comparison-adjusted funnel` |

---

## Data Formats / 数据格式

| Type | Required | Example |
|------|----------|---------|
| Binary arm-level | study, treatment, n, events | study A, DrugX, 100, 25 |
| Continuous arm-level | study, treatment, n, mean, sd | study A, DrugX, 50, 12.3, 2.1 |
| Survival arm-level | study, treatment, n, time, status | study A, DrugX, 80, 12.5, 1 |
| Contrast-level (change) | study, treatment, mean_diff, se, n | study A, DrugX vs PBO, 2.1, 0.5, 50 |

---

## References / 引用

- What works best depends on research question: multinma offers population adjustment; gemtc is the classic frequentist-Bayesian bridge
- multinma:抗老,



继续创建其他引用文件。
</longcat_think>
