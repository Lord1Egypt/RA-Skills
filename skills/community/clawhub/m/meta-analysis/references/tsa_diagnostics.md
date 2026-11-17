# TSA & Model Diagnostics / 诊断序贯分析与模型诊断

## run_tsa() — Trial Sequential Analysis / 试验序贯分析

> 在累积 Meta 分析中控制 I 类错误（类似 RCT 期中监测）。
> ⚠️ **注意**：`meta` 包并**不存在** `tes()` 函数（历史文档误写）。本技能提供**自实现**的
> `run_tsa()`（Wetterslev 2017 标准公式 + O'Brien-Fleming 监测边界），无需任何外部包。

```r
source("src/r_engine/advanced_functions.R")

# es_data 需含 yi(效应量) 与 vi(方差)；labels 为研究标签(按时间排序)
# ---- 连续型结局（用最小临床重要差 d，SMD 尺度）----
ts <- run_tsa(
  es_data, labels,
  effect_type = "continuous",
  d      = 0.2,          # 最小临床重要差 (SMD)
  alpha  = 0.05,
  power  = 0.80,
  side   = "two"         # 双侧
)

# ---- 二分类结局（用预期 OR 与两组事件率）----
ts2 <- run_tsa(
  es_data, labels,
  effect_type = "binary",
  or          = 0.80,    # 预期效应 OR
  p_con       = 0.10,    # 对照组事件率
  p_exp       = 0.08,    # 试验组事件率
  n_per_study = n_vec,   # 各研究样本量(向量)
  alpha = 0.05, power = 0.80
)

# 返回值：$RIS(所需信息量) $accrued(已累积) $info_frac $cum_Z(累积Z) 
#         $crossed(是否越界) $reached_RIS $conclusion(结论文本) $plot(ggplot)
print(ts$conclusion)
if (!is.null(ts$plot)) print(ts$plot)   # Z 曲线 + O'Brien-Fleming 边界
```

### TSA interpretation / 解读
- 累积 Z 曲线越过监测边界 → 效应确证（无需更多研究）
- 累积 Z 曲线越过无效边界 → 判定无效
- 所需信息量 RIS > 已累积样本 → 证据不足，需更多研究
- RIS = 达到目标把握度所需的“等效试验规模”

---

## baujat() — Heterogeneity Source / 异质性来源诊断

```r
b <- baujat(res)
print(b)
plot(b)
```

### Interpretation / 解读
- X-axis: contribution to overall heterogeneity (Q_i)
- Y-axis: influence on overall result (overall estimate change when removed)
- Studies in upper-right → high contribution + high influence → check these studies

---

## drapery() — α-Percept Drapery / α-稳健性图

```r
library(meta)
drapery(res, type = "zvalue", print = TRUE)
```

### Interpretation / 解读
- Shows how significance (z-value) changes for varying α levels simultaneously
- More robust than single-α forest plot (avoids α-cutoff dichotomy)

---

## bootmeta() — Bootstrap Meta / Bootstrap重抽样

```r
library(bootmeta)

# Non-parametric bootstrap (DL alternative with small samples)
bm <- bootmeta(res, B = 1000, worker = 4)
plot(bm)
```

- Confidence intervals via percentile bootstrap
- More robust than REML when k<10

---

## Selection Model Extensions / 选择模型扩展

```r
library(weightr)

# Weight-function model for publication bias
wt <- weightfunct(
  effect = df$yi,
  v = df$vi,
  steps = c(0.005, 0.01, 0.05, 0.1, 0.25, 0.35, 0.5, 1)
)
summary(wt)
plot(wt)
```

### Interpretation / 解读
- p-value distribution is asymmetric → publication bias
- Can adjust pooled estimate for publication bias

---

## References / 引用
- Wetterslev J, et al. (2008). Trial sequential analysis may establish when firm evidence is reached in cumulative meta-analysis. *J Clin Epidemiol*, 58(1), 6-13.
- Baujat B, et al. (2002). A graphical method for exploring heterogeneity in meta-analyses. *Stat Med*, 21(22), 2641-2652.
- Higgins JPT, Spiegelhalter DJ. (2002). Being sceptical about meta-analyses: a Bayesian perspective on triangular trials. *Stat Med*, 21(3), 417-437.
- Bootmeta CRAN package
