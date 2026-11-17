# esc / clubSandwich / robumeta Reference Manual

## I. esc Effect Size Package

### 1.1 Overview

`esc` 包（Effect Size Calculation）提供从原始统计量到标准效应量的转换，是 meta 分析数据准备阶段的利器。

### 1.2 Main Functions

| 函数 | 输入 | 输出 |
|------|------|------|
| `esc_mean_sd()` | 均值/SD/n | Cohen's d + 方差 |
| `esc_t()` | t 值/n | Cohen's d |
| `esc_F()` | F 值(df1=1)/n | Cohen's d |
| `esc_rcor()` | 相关系数 r/n | d + 方差 |
| `esc_or()` | OR + SE | d (logOR 变换) |
| `esc_chisq()` | χ²/n | w (效应量) |

### 1.3 Conversion Paths

```
原始数据
   ├── 均值 → Cohen's d → Hedges' g → logOR / Fisher's z
   ├── t/F → Cohen's d → ...
   ├── r → Fisher's z → Cohen's d → logOR
   └── OR/2×2 → logOR → Cohen's d
```

### 1.4 Cohen's d → Hedges' g 校正

```r
esc_d_to_g <- function(d, n1, n2) {
  df <- n1 + n2 - 2
  J <- 1 - 3 / (4 * df - 1)
  g <- J * d
  vi_g <- J^2 * (n1 + n2) / (n1 * n2) + g^2 / (2 * (n1 + n2))
  data.frame(yi = g, vi = vi_g, J = J)
}
```

---

## II. robumeta Robust Variance Estimation

### 2.1 Core Idea

- **问题**：同一研究产生多个相关效应量，传统元分析假设独立性 → 方差估计偏小
- **解决**：`robumeta` 基于 Huber-White 三明治方差估计器，仅假设研究间独立
- **tau²估计**：使用 Fisher-z 小样本校正（Hunter-Schmidt 类）
- **小样本p值**：使用 Satterthwaite 自由度近似

### 2.2 Common Settings

| Setting | 描述 | 何时用 |
|---------|------|--------|
| `"Tech2"` | 默认（默认小样本校正） | 10+ 研究 |
| `"Tech3"` | 无小样本校正 | 大样本研究 |
| `"Small"` | 强制小样本校正 | < 10 项研究 |
| `"Fisher"` | Fisher-z 变换版 | 效应量为 OR/HR |

### 2.3 Complete Workflow

```r
library(robumeta)

# 1. 数据格式
data <- data.frame(
  study_id = c("A", "A", "B", "C", "C", "C"),
  effect_id = c("e1", "e2", "e1", "e1", "e2", "e3"),
  yi = c(0.5, 0.7, 0.3, 0.8, 0.6, 0.9)
)

# 2. 拟合
fit <- robu(yi ~ 1, data = data, studynum = study_id)

# 3. 输出
summary(fit)
confint(fit)

# 4. 质量检查
cat(sprintf("Robust tau²: %.3f\n", fit$tau2))
cat(sprintf("Robust SE: %.4f\n", fit$SE))
cat(sprintf("Satterthwaite df: %.1f\n", fit$dfs))
cat(sprintf("Robust p-value: %.4f\n", fit$pval))
```

### 2.4 Meta-Regression (Multiple Covariates)

```r
# 多变量元回归
fit_mod <- robu(
  yi ~ year + quality_score + allocation_concealment,
  data = robu_data,
  studynum = study_id,
  rho = 0.8,
  small = TRUE
)

# 小样本 F 检验（含交互项）
anova(fit_mod)
```

### 2.5 Forest Plot

```r
library(ggplot2)

# 使用模型拟合值
pred <- predict_robu(fit)

ggplot(mapping = aes(x = estimate, y = study_id)) +
  geom_point() +
  geom_errorbarh(aes(xmin = ci.lb, xmax = ci.ub), height = 0.2) +
  geom_vline(xintercept = 0, linetype = "dashed")
```

---

## III. clubSandwich + metafor Combined

### 3.1 Why Combine

`rma.mv()` 可拟合正确的层次结构，但渐近 SE 在小样本下过于乐观。  
`clubSandwich` 提供 **HC0-HC5** 和 **CR0-CR4** 校正，其中 **CR2** 被广泛推荐。

### 3.2 CR Correction Types

| 类型 | 描述 | 小样本恢复 |
|------|------|-----------|
| CR0 | 基础稳健（无校正） | ❌ 在小样本下偏乐观 |
| CR1 | 自由度校正 | ✅ |
| CR2 | **Kauermann-Carroll + 小样本改进** | ✅✅ **推荐** |
| CR3 | Jackknife | ✅ |
| CR4 | 高杠杆调整 | ✅ |

### 3.3 Complete Workflow

```r
library(metafor)
library(clubSandwich)

# Step 1: 构建 V 矩阵（见 effect_size_conversions.R）
V_list <- build_V_matrix_manual(data, rho = 0.8)

# Step 2: rma.mv 多水平拟合
mv_fit <- rma.mv(
  yi = yi,
  V = bldiag(V_list),    # 转换为分块对角矩阵
  random = ~ 1 | study_id / effect_id,
  data = data,
  method = "REML",
  test = "t"
)

# Step 3: clubSandwich CR2 稳健 SE
robust <- vcovCR(mv_fit, cluster = data$study_id, type = "CR2")
robust_test <- coef_test(mv_fit, vcov = robust, test = "Naive")

# Step 4: 对比
cat("Standard:", round(mv_fit$pval, 4), "\n")
cat("Robust:  ", round(robust_test$p_value[1], 4), "\n")
```

### 3.4 配合 impute.vcov()

当只有 V 矩阵的近似值（或缺失相关性）时，用 `impute.vcov()` 基于采样分布填充：

```r
# 对每个研究，构建研究内协方差矩阵的估计
V_imputed <- impute.vcov(
  vcov.data = data$yi,
  cluster = data$study_id,
  r = 0.8  # 假设的相关系数
)

# 然后 bldiag(V_imputed) 用于 rma.mv
```

---

## IV. Estimation of Within-Study Effect Correlation

### 4.1 Obtain ρ from Study Reports

同一研究内多个结局的效应量相关性（ρ）可通过以下方法获取：

1. **研究报告**：少数研究会报告直接相关矩阵
2. **重测信度**：心理测量学研究中的 0.5-0.8
3. **敏感性分析**：ρ = 0.2, 0.4, 0.6, 0.8 多种情况
4. **estomega**: `robumeta` 可内部估计研究内相关

### 4.2 Sensitivity Analysis Framework

```r
# 不同 rho 下的结果稳定性
rho_values <- c(0.2, 0.4, 0.6, 0.8)
lapply(rho_values, function(r) {
  V <- build_V_matrix_manual(data, rho = r)
  fit <- rma.mv(yi = yi, V = bldiag(V),
                 random = ~ 1 | study_id / effect_id,
                 data = data, method = "REML")
  data.frame(rho = r, b = fit$b, p = fit$pval)
}) |> do.call(what = rbind)
```

---

## V. Checklist

### Necessity Check Before Using robumeta

- [ ] 是否有研究产生 >1 个效应量？
- [ ] 研究数量 < 20？（小样本下 RVE 更重要）
- [ ] 是否计划纳入协变量（元回归）？
- [ ] 效应量度量是否适合 Fisher-z 变换？（OR/HR 适合，OR/SMD 需考虑）

### Preparation Before Using clubSandwich

- [ ] 已用 `rma.mv()` 拟合多水平模型？
- [ ] 已构建/估计 V 矩阵（或愿意用 `impute.vcov()`）？
- [ ] 研究结果含聚类结构（研究内效应量 >1）？
- [ ] 关注小样本性能？（研究数 < 30 时强烈推荐）

---

## VI. Recommended Use Cases

| 场景 | 推荐包 | R 函数 |
|------|--------|--------|
| 快速效应量计算（均值→d） | esc | `esc_mean_sd()` |
| 效应量变换（d→logOR） | esc / 手动 | `esc_or()` / 线性变换 |
| 多结局/多臂依赖数据（10-30研究） | robumeta | `robu()` |
| 多结局（>30研究）+ 元回归 | metafor + clubSandwich | `rma.mv` + `vcovCR` |
| V 矩阵不确定时的探索 | robumeta | 多种 rho 敏感性 |
| 发表偏倚检验（稳健版） | robumeta | `robu()` 后 `regtest()` |

---

## VII. Citation Format

1. **esc**: Lüdecke D (2019). esc: Effect Size Computation for Meta-Analysis. R package version 0.5.1.

2. **robumeta**: Fisher Z, Tipton E (2015). robumeta: An R-package for robust variance estimation in meta-analysis. arXiv preprint arXiv:1503.02220.

3. **clubSandwich**: Pustejovsky J (2022). clubSandwich: Cluster-Robust (Sandwich) Variance Estimators with Small-Sample Corrections. R package version 0.5.10.

4. **Viechtbauer & Cheung** (2010): Outlier and influence diagnostics for meta-analysis. *Research Synthesis Methods*, 1(2), 112-125.
