# 片段类型：语法

## 原文片段

To test for measurement invariance across time, we first estimated longitudinal correlated factor models for each personality trait, LS and WS separately. For example, we specified a seven-factor (i.e., seven available waves) model for openness, with each factor representing openness at the corresponding measurement occasion. Each personality factor was estimated based on the ten corresponding items at each measurement occasion. For LS and WS, we used a model with 11 and 12 factors (i.e., 11 and 12 available waves, respectively) measured by five items each. For all models, we added residual correlations between the same items across measurement waves. Models were estimated in R using the lavaan package (Rosseel, 2012) and full information maximum likelihood estimation to account for missing values.

## 来源文献

Olaru, G., et al. (2023). The link between personality, global, and domain-specific satisfaction across the adult lifespan. Journal of Personality and Social Psychology.

## 适配诊断点

建模细节一般过去时（we first estimated / we specified / we added / were estimated in R）贯穿，波次与因子数一一对应（seven-factor = seven waves）、残差相关处理与 FIML 缺失处理一并交代，是 SEM 建模描述的语法范本。
