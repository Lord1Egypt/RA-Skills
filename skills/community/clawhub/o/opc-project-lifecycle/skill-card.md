## Description: <br>
OPC项目全流程管理，每个项目创建独立档案，覆盖从立项到交付的完整生命周期. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OPC teams and project operators use this skill to create project archives, track lifecycle stages, coordinate handoffs with related OPC skills, and produce stage reports, dashboards, reviews, and achievement records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent project archives can collect sensitive client, financial, legal, or confidential business information. <br>
Mitigation: Review before writes or syncs, redact sensitive fields, and define retention and deletion rules before using real project data. <br>
Risk: Cross-skill coordination can pass project data into other OPC workflows. <br>
Mitigation: Confirm the data scope for each handoff and require approval before sharing confidential material with downstream skills. <br>
Risk: Privileged skill creation or patching behavior could alter operational workflows. <br>
Mitigation: Disable skill_manage create or patch workflows, or require separate explicit approval before they run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/golngod/opc-project-lifecycle) <br>
- [README.md](README.md) <br>
- [SOP操作手册.md](references/SOP操作手册.md) <br>
- [快速启动检查清单.md](references/快速启动检查清单.md) <br>
- [成就徽章数据库.md](references/成就徽章数据库.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown project archives, templates, checklists, dashboards, stage reports, and status updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update persistent local project records and coordinate data across related OPC skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
