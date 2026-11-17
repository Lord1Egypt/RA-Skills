# 片段类型：逻辑（数据结构的建模选择与理由）

## 原文片段

> The study design implies a multilevel data structure in which the individual scores are nested within the 95 different domains. Furthermore, participants were allowed to take part in the study repeatedly, in which case the same participant was assigned to a different domain, leading to additional dependency in the data. Although theoretically possible, we decided against reporting cross-classified multilevel models for several reasons, opting instead for traditional multilevel models. In the following sections, we outline how both our hypotheses translate into multilevel models.

## 来源文献

Urban, Koch, & Rothermund (2024), Study 2, Data Analysis section. *The Implicit Association Test: A Methodological Investigation of the Relationship Between Test Difficulty and Criterion Validity.* https://osf.io/pcjwf/

## 适配诊断点

- 分析前先陈述数据结构的嵌套性质（个体嵌套于 95 个领域，且存在重复测量造成的额外依赖），为统计模型选择提供数据层面的理由。
- 对"理论上可能但最终未采用"的备选模型（cross-classified multilevel models）明确交代取舍原因并指向脚注，体现方法选择的透明性而非默认路径。
- "In the following sections, we outline how both our hypotheses translate into multilevel models" 用一句话建立假设与统计模型的对应关系，是假设-模型映射的标准写法。
