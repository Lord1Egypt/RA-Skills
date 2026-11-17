# 片段类型：逻辑（倾向值匹配的算法决策链）

## 原文片段

> The propensity score was calculated by regressing various covariates on the binary treatment variable (divorce). The predictors included life satisfaction and satisfaction with health and income as well as many other variables associated with divorce and/or life satisfaction (a full list is included in Table 1). Only 32 of the 787 divorcees had missing data on one or more covariates included in the propensity score matching model in the year of marriage. We imputed the very few missing values using the mean across all responses. After propensity-score matching, we replaced the imputed variables with the original variables with missing data. For each divorcee, the matching model used a nearest neighbor algorithm to find the three best matches based on their propensity scores (Thoemmes & Kim, 2011). We used matching with replacement, which means that respondents in the control sample were allowed to be included more than once. This approach ensured that each divorcee could be matched to the nearest control, even if this control was already included in a previous match. Compared with matching without replacement, this approach reduces the risk of matching divorcees to controls that are quite different in their propensity scores (Dehejia & Wahba, 2002). We used a tolerance level on the maximum propensity-score distance between matches using a caliper width of .2 SDs of the logit of the propensity score (Austin, 2011).

## 来源文献

van Scheppingen, M. A., & Leopold, T. (2020), Method (Data Analyses, Propensity-Score Matching). *Trajectories of Life Satisfaction Before, Upon, and After Divorce: Evidence From a New Matching Approach.* Journal of Personality and Social Psychology, 119(6), 1444-1458.

## 适配诊断点

- 匹配流程的每个决策都有理由：缺失值处理（均值插补 + 匹配后还原）、匹配算法（nearest neighbor, 3 best matches）、是否放回（with replacement 及其利弊对比）、卡尺宽度（.2 SDs of logit）。
- 方法选择用比较句式论证（"Compared with matching without replacement, this approach reduces the risk of ..."），并引用方法学文献（Thoemmes & Kim, 2011; Dehejia & Wahba, 2002; Austin, 2011）。
- 关键概念先定义（"The propensity score reflects the probability that a respondent will divorce or not, given the values of all covariates"），再进入操作细节。
- 每一步参数都可复现：插补方式、邻居数（3）、caliper 宽度（.2 SD）、算法出处。
