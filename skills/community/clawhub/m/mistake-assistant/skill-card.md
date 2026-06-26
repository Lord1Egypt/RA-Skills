## Description: <br>
智能错题管理助手，支持错题记录、分类整理、复习提醒、统计分析和导出分享。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students use this skill to record missed questions, organize them by subject and topic, schedule review, inspect weak areas, and export mistake notebooks for study. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores private study records in local files. <br>
Mitigation: Use it in a private workspace and review stored data before syncing or sharing the workspace. <br>
Risk: Security review flagged file writes as too loosely scoped for a skill that stores and exports study records. <br>
Mitigation: Prefer a revised version that constrains writes to mistake-data/ and mistake-exports/ before broad use. <br>
Risk: Exported HTML may include copied untrusted content from study materials. <br>
Mitigation: Do not open exported HTML containing untrusted content unless the content has been reviewed or escaped. <br>
Risk: Export and delete actions can affect local study records. <br>
Mitigation: Confirm export paths and deletion requests before running those actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallkeyboy/mistake-assistant) <br>
- [艾宾浩斯遗忘曲线复习算法](references/forgetting_curve.md) <br>
- [错题录入模板](references/templates.md) <br>
- [Subject taxonomy](references/subjects.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON, HTML, PDF, and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent local study records under mistake-data/ and exports notebooks under mistake-exports/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
