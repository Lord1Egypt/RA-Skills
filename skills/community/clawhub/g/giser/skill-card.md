## Description: <br>
GIS_SKILL_V1.0 is a Chinese-language GIS knowledge-base skill that helps agents answer surveying, mapping, geospatial standards, GIS software, data processing, automation, and project troubleshooting questions. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[leo-gissss](https://clawhub.ai/user/leo-gissss) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
Developers, GIS analysts, surveyors, and geospatial project teams use this skill to retrieve structured guidance on coordinate systems, Chinese surveying standards, ArcGIS/QGIS/FME/CASS workflows, WebGIS, spatial databases, LiDAR, remote sensing, automation, and GIS project quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes persistent self-evolution, auto-search, feedback logging, and knowledge-base mutation behavior. <br>
Mitigation: Disable or require explicit approval for self-evolution, auto-search, feedback logging, and skill-file updates before deployment. <br>
Risk: The skill can guide agents toward backup, deployment, file, database, and command examples that may affect local data or systems. <br>
Mitigation: Require human review, backups, and least-privilege execution before running generated commands or modifying files and databases. <br>
Risk: The security scan labels the release suspicious because broad triggers can start active maintenance workflows. <br>
Mitigation: Use the skill as a reviewed GIS reference assistant unless active maintenance behavior is explicitly needed and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leo-gissss/giser) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [License file](artifact/LICENSE.txt) <br>
- [National surveying standards module](artifact/references/05_国家测绘标准体系.md) <br>
- [ArcGIS Pro module](artifact/references/12_ArcGIS_Pro.md) <br>
- [QGIS module](artifact/references/13_QGIS.md) <br>
- [Python GIS ecosystem module](artifact/references/21_Python_GIS生态.md) <br>
- [Self-evolution feedback mechanism](artifact/references/37_自进化反馈机制.md) <br>
- [OGC standards handbook](artifact/references/40_OGC国际标准速查手册.md) <br>
- [QGIS Processing algorithm handbook](artifact/references/44_QGIS_Processing算法速查手册.md) <br>
- [GIS Agent skill design patterns](artifact/references/45_GIS_Agent技能设计范式.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prose with tables, checklists, code snippets, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose GIS workflows, quality checks, file operations, scripts, and software-specific commands that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
