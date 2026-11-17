## Description:

GIS_SKILL_V1.0 is a modular GIS knowledge-base skill for agents covering coordinate systems, surveying and mapping standards, desktop GIS tools, automation, spatial databases, remote sensing, WebGIS, 3D GIS, quality checks, and practical troubleshooting.

This skill is for research and development only.

## Publisher:

[leo-gissss](https://clawhub.ai/user/leo-gissss)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

GIS practitioners, surveying and mapping specialists, developers, and agents use this skill as a structured reference for planning GIS workflows, selecting tools and formats, generating code or shell-command guidance, checking data quality, and avoiding known geospatial processing pitfalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a self-evolution system that can persist user text, search externally, and rewrite skill or reference files without clear consent or review.

Mitigation: Use it as a read-only GIS reference by default; disable self_evolution_enabled, auto_search_enabled, and feedback_detection_enabled unless the user deliberately enables them.

Risk: Feedback logging can capture user-provided text.

Mitigation: Require explicit user approval before recording feedback or incorporating user text into skill files.

Risk: The artifact contains shell, HTTP, and credential-handling examples that may be unsafe if copied directly into production.

Mitigation: Review and adapt examples before use; avoid copying unsafe shell or credential examples into production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leo-gissss/skills/giser)
- [Basic GIS theory and positioning](references/01_基础理论与学科定位.md)
- [Coordinate systems and projections](references/02_坐标系统与投影.md)
- [Data models and formats](references/03_数据模型与格式.md)
- [Chinese coordinate-system practice](references/04_中国三大坐标系实战.md)
- [Surveying and mapping standards](references/05_国家测绘标准体系.md)
- [Data production workflow specifications](references/06_数据生产流程规范.md)
- [Quality inspection and acceptance standards](references/07_质量检查与验收标准.md)
- [Result delivery and archiving specifications](references/08_成果汇交与归档规范.md)
- [New basic surveying and mapping entities](references/09_新型基础测绘实体规范.md)
- [Industry workflow diagrams](references/10_测绘建库行业标准流程图集.md)
- [ArcGIS Pro](references/12_ArcGIS_Pro.md)
- [QGIS](references/13_QGIS.md)
- [CASS 11.0](references/14_CASS11.0.md)
- [iData Data Factory](references/15_iData_数据工厂.md)
- [SuperMap iDesktopX](references/16_SuperMap_iDesktopX.md)
- [Global Mapper](references/17_GlobalMapper.md)
- [FME Form and Flow](references/18_FME_Form与Flow.md)
- [Multi-source data fusion](references/19_多源数据融合.md)
- [GIS resource sharing](references/20_GIS资源共享.md)
- [Python GIS ecosystem](references/21_Python_GIS生态.md)
- [Spatial databases](references/22_空间数据库.md)
- [WebGIS development](references/23_WebGIS开发.md)
- [Remote sensing and Google Earth Engine](references/24_遥感与GEE.md)
- [3D GIS and digital twins](references/25_三维GIS与数字孪生.md)
- [WorkBuddyGIS AddIn development](references/26_WorkBuddyGIS_AddIn开发.md)
- [AI and GIS](references/27_AI_GIS.md)
- [Project case collection](references/28_项目案例集.md)
- [GIS troubleshooting and anti-pattern library](references/29_避坑库.md)
- [GIS and CAD conversion](references/30_GIS↔CAD数据转换.md)
- [Learning paths and certification resources](references/31_学习路径与认证资源.md)
- [GNSS surveying and engineering applications](references/32_GNSS测量与工程应用.md)
- [Spatial analysis and statistics](references/33_空间分析与统计.md)
- [Expert batch processing and automation](references/35_专家级批量处理与自动化实战指南.md)
- [LiDAR360 point-cloud processing](references/36_LiDAR360_点云处理软件.md)
- [Self-evolution feedback mechanism](references/37_自进化反馈机制.md)
- [ArcGIS Pro 3.7 new features](references/38_ArcGIS_Pro_3.7_新功能详解.md)
- [R GIS ecosystem](references/39_R语言GIS生态.md)
- [OGC standards quick reference](references/40_OGC国际标准速查手册.md)
- [Modern GIS data-processing pipelines](references/41_现代GIS数据处理管道.md)
- [Multilanguage geospatial library ecosystem](references/42_多语言地理空间库生态.md)
- [Format-selection decision trees and anti-patterns](references/43_格式选择决策树与反模式.md)
- [QGIS Processing algorithm quick reference](references/44_QGIS_Processing算法速查手册.md)
- [GIS agent skill design patterns](references/45_GIS_Agent技能设计范式.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, command examples, checklists, workflow plans, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local skill files and may propose file changes or external searches only when the user explicitly approves those behaviors.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version: 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
