# 片段类型：写作规范（多数据源、IRB 豁免与修订预注册的透明度）

## 原文片段

> Transparency and Openness. This research relied on three data sets. A digitized version of the data on prewar economic performance (Deutsches Reich Statistisches Reichsamt, 1941) is publicly available in the Harvard dataverse: https://doi.org/10.7910/DVN/MIE4XB. A digitized version of the data on the post–Second World War destruction levels of West German municipalities provided by Gassdorf and Langhans-Ratzeburg (1950) is available online in the supplemental files of Halbmeier and Schröder (2025). Data from the German SOEP Study (Socio-Economic Panel, 2023) are available to research institutes and universities for research purposes from the SOEP Research Data Centre. [...] Since we used archival data available in the public domain and collected in compliance with high ethical standards, we are exempt from an Institutional Review Board approval. [...] Data preparation and analyses were done in R, Version 4.3. (R Core Team, 2024) with the packages tidyverse (Wickham, 2019), haven (Wickham et al., 2015), sf (Pebesma, 2018; Pebesma & Bivand, 2023), fixest (Bergé, 2018), flextable (Gohel & Skintzos, 2017), gtsummary (Sjoberg et al., 2021), [...] This study's hypotheses and analysis strategy were preregistered at https://osf.io/mqp4z/ [...]. Of note, our analytical strategy evolved during the revision process in response to reviewer requests, including changes to the set of covariates, the inclusion of process analyses, and robustness checks using earlier data. Importantly, all reviewer-requested analyses were preregistered prior to being conducted. Both the original and the revised preregistrations are publicly available on the Open Science Framework. [...] All analytical R code and additional materials are provided on the Open Science Framework project site at https://osf.io/9cwqy/ [...].

## 来源文献

Entringer, T. M., Halbmeier, C., Buchinger, L., & Reitz, A. K. (2026), Method (Transparency and Openness). *Within-Nation Variation in War Exposure and Psychological and Physical Adjustment.* Journal of Personality and Social Psychology, 131(2), 355-379. https://doi.org/10.1037/pspp0000601

## 适配诊断点

- 多数据源可用性逐一交代：每个数据集给出存放位置（Harvard dataverse / 补充材料 / SOEP 数据中心的申请流程链接），开放程度分级说明。
- IRB 豁免的理由具体（archival public-domain data + ethical standards），非简单省略伦理声明。
- 分析环境完整报告：R 版本（4.3, R Core Team, 2024）+ 全部软件包（逐个带引用），可复现性最大化。
- 修订预注册的透明处理是亮点：分析策略因审稿演变 → 所有新分析先预注册再执行 → 原始与修订版都公开 → 所有偏离在文中标注，预注册诚信的完整闭环。
