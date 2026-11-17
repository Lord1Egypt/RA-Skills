# 片段类型：写作规范（数据获取、伦理豁免与可复现材料共享）

## 原文片段

> The current study made use of publicly available de-identified data. Therefore, the current study's analyses were considered exempt by the University of Amsterdam's Institutional Review Board. To the best of our knowledge, no published studies have examined changes in life satisfaction during divorce based on a matched control sample. Yet, German SOEP is widely used in studies on the consequences of divorce and other major life events on life satisfaction.
>
> We used data from 33 waves of the German SOEP-long (Version 33, release 2018; Wagner, Frick, & Schupp, 2007). The SOEP is a household panel survey in which each household member age 17 and older is interviewed separately. Annual measures of life satisfaction and marital status were available from 1984 to 2016, allowing us to model year-to-year changes in life satisfaction across the divorce process. Moreover, the SOEP data provided a large sample of respondents followed from marriage until divorce. The SOEP data is subject to data protection laws of the Federal Republic of Germany; thus, the data cannot be made public. However, free access is granted to all scientific researchers who sign a contract with the German Institute for Economic Research (DIW Berlin).
>
> The sample used in the current study can be recreated from the original SOEP-long file (v33) by using the Stata do-file available on the Open Science Framework (OSF).

## 来源文献

van Scheppingen, M. A., & Leopold, T. (2020), Method (Data and Sample). *Trajectories of Life Satisfaction Before, Upon, and After Divorce: Evidence From a New Matching Approach.* Journal of Personality and Social Psychology, 119(6), 1444-1458.

## 适配诊断点

- 伦理合规透明：公开去标识数据 + 伦理豁免声明（IRB）一并交代。
- 数据来源描述完整：面板名称、版本（SOEP-long Version 33, release 2018）、调查结构（每户 17 岁以上成员单独访谈）、覆盖年份（1984-2016）。
- 数据可及性说明详尽：为何不能公开（数据保护法）+ 研究者如何获取（与 DIW Berlin 签约）+ 联系渠道。
- 可复现性安排到位：明确说明样本可由原始文件 + Stata do-file 在 OSF 上复现，分析代码共享路径清晰。
