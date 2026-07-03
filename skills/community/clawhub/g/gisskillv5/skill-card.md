## Description: <br>
GIS_SKILL_V5.0 is a comprehensive GIS knowledge and workflow skill covering coordinate systems, surveying and mapping standards, GIS software workflows, automation scripts, quality inspection, GIS/CAD conversion, remote sensing, point clouds, and self-evolution routines. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[leo-gissss](https://clawhub.ai/user/leo-gissss) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
Developers, GIS analysts, and surveying or mapping teams use this skill to plan and execute GIS data processing workflows, select coordinate systems and software workflows, generate scripts or checklists, and validate outputs against GIS and mapping standards. <br>

### Deployment Geography for Use: <br>
Global; many workflows and reference materials are tailored to China surveying and mapping standards. <br>

## Known Risks and Mitigations: <br>
Risk: The security review identifies active GIS automation and a self-evolving knowledge system with external update checks. <br>
Mitigation: Install only when active automation is desired; disable self-evolution, auto-search, and update checks unless they are explicitly needed. <br>
Risk: The security review notes feedback retention and package rewriting behavior. <br>
Mitigation: Review feedback retention settings, keep backups, and approve any knowledge-base or package updates before promoting them. <br>
Risk: The security review notes possible source-data mutation and GIS conversion behavior. <br>
Mitigation: Run scripts only on copies of GIS data and keep original datasets read-only. <br>
Risk: Topology repair, 3D conversion, coordinate transformation, and quality inspection outputs can be wrong if assumptions or local standards are mismatched. <br>
Mitigation: Manually validate spatial outputs, CRS choices, tolerances, and acceptance reports before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leo-gissss/skills/gisskillv5) <br>
- [GIS_SKILL_V5.0 skill definition](artifact/SKILL.md) <br>
- [V5 constitution](artifact/V5_CONSTITUTION.md) <br>
- [Version matrix](artifact/VERSION_MATRIX.md) <br>
- [Package manifest](artifact/PACKAGE_MANIFEST.json) <br>
- [GeoEvolve self-evolution engine](artifact/geo_evolve/README.md) <br>
- [GIS automation scripts](artifact/scripts/README.md) <br>
- [Coordinate systems and projections](artifact/references/02_坐标系统与投影.md) <br>
- [National surveying and mapping standards](artifact/references/05_国家测绘标准体系.md) <br>
- [Quality inspection and acceptance standards](artifact/references/07_质量检查与验收标准.md) <br>
- [Python GIS ecosystem](artifact/references/21_Python_GIS生态.md) <br>
- [GIS and CAD data conversion](artifact/references/30_GIS↔CAD数据转换.md) <br>
- [Self-evolving feedback mechanism](artifact/references/37_自进化反馈机制.md) <br>
- [OGC standards quick reference](artifact/references/40_OGC国际标准速查手册.md) <br>
- [GIS agent skill design patterns](artifact/references/45_GIS_Agent技能设计范式.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown prose with code blocks, command snippets, structured checklists, and file-oriented workflow outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce GIS processing plans, scripts, quality reports, logs, and acceptance checklists; spatial outputs and conversion results require domain review.] <br>

## Skill Version(s): <br>
5.0.2 (source: SKILL.md frontmatter and PACKAGE_MANIFEST.json); ClawHub release version 1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
