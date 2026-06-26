## Description: <br>
n8n工作流自动化工具包，包含上百种常用工作流模板，支持一键导入、批量管理、定时任务配置、工作流备份恢复等功能，开箱即用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to generate n8n CLI commands and workflow assets for importing templates, backing up workflows, configuring schedules, and monitoring workflow failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an n8n API key and can make persistent changes to workflows. <br>
Mitigation: Use a least-privilege n8n API key, test against a non-production n8n instance, and review workflow changes before enabling imported or scheduled workflows. <br>
Risk: Import, schedule, and backup operations can affect existing automation state or overwrite expected workflow behavior. <br>
Mitigation: Back up workflows before import or scheduling actions and validate cron expressions and workflow names before running commands. <br>
Risk: Monitoring alerts may send workflow error details to external webhook destinations. <br>
Mitigation: Send alerts only to trusted webhook destinations and avoid exposing sensitive execution details in shared channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/n8n-workflow-cn) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/paudyyin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python workflow tooling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce n8n API requests, workflow JSON backups, cron expressions, and webhook alert configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
