## Description: <br>
全流程项目管理工具，用于梳理项目关键节点、管理参与部门与任务排期、跟踪KPI完成度、生成定期报告、发送进度提醒邮件、创建可视化看板。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmywangjimmy](https://clawhub.ai/user/jimmywangjimmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Project managers, PMO staff, and cross-functional teams use this skill to structure projects, track departments, milestones, tasks, KPIs, and risks, and generate recurring project reports, visual boards, and reminder drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe project IDs or project JSON data can affect local files because the skill reads and writes project, report, board, and email-draft files on disk. <br>
Mitigation: Use trusted project IDs and trusted project JSON only, and run the skill in a workspace where project-management output paths are expected. <br>
Risk: Generated reports, boards, and email drafts may expose project status, assignees, blockers, KPIs, or recipient details. <br>
Mitigation: Keep generated files private and review their contents before sharing or sending them outside the intended project audience. <br>
Risk: Generated HTML boards may include unescaped project data. <br>
Mitigation: Avoid opening HTML boards created from imported or shared project data until HTML escaping and path confinement issues are fixed. <br>


## Reference(s): <br>
- [Project Flow Manager reference documentation](references/api_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/jimmywangjimmy/project-flow-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON project files, HTML or Markdown boards, text email drafts, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local project-management files under project, report, board, and email-draft directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
