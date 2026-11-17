# 片段类型：逻辑（分析方法的决策链与替代方案比较）

## 原文片段

> Second, we addressed our two main research questions: (RQ1) the long-term association between early-childhood war exposure and late-life adjustment, and (RQ2) the intergenerational impact of parents' early-childhood war exposure on their children's midlife adjustment. We used ordinary least squares regression with standard errors clustered at the municipality level. This approach aligns with prior studies using similar designs (e.g., Akbulut-Yuksel, 2017; Halbmeier & Schröder, 2025). We opted against multilevel modeling due to the small number of observations per cluster in our data (Mcluster size = 1.67 [place-of-residence sample] to 2.32 [birthplace sample], range = 1–192), which can lead to convergence problems and biased standard errors (McNeish, 2014). For RQ1, we regressed psychological and physical adjustment in 2012 on individuals early-life war exposure, controlling for prewar population size and regional economic performance.

## 来源文献

Entringer, T. M., Halbmeier, C., Buchinger, L., & Reitz, A. K. (2026), Method (Analytical Procedure). *Within-Nation Variation in War Exposure and Psychological and Physical Adjustment.* Journal of Personality and Social Psychology, 131(2), 355-379. https://doi.org/10.1037/pspp0000601

## 适配诊断点

- 方法选择显式给出替代方案及其被否理由：OLS + 聚类标准误 vs. 多层模型，量化依据（Mcluster size = 1.67–2.32）→ 后果（收敛问题、标准误偏倚）→ 文献支撑（McNeish, 2014）。
- 选用方法与既有研究对齐（aligns with prior studies ...），方法有先例背书。
- 研究问题（RQ1/RQ2）与分析模型（回归方程）逐字对应，回归内容明确写出（DV、IV、控制变量）。
- 分析分两步（先暴露单独、再加前测控制变量），模型渐进策略清晰。
