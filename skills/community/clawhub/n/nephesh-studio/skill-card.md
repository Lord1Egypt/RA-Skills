## Description: <br>
Nephesh Studio provides an OpenClaw multi-agent team workflow with specialist roles, CEO-led coordination, persistent role knowledge files, project isolation, QA review, and optional daily checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raydoomed](https://clawhub.ai/user/raydoomed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to coordinate complex OpenClaw projects through a structured team of planning, management, engineering, content, data, design, HR, and QA roles. It is intended for persistent project workflows where the agent creates project files, delegates subagent tasks, reviews outputs, and records lessons learned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent agent behavior through role knowledge files and project records. <br>
Mitigation: Review and approve changes to SOUL.md, project directories, learning files, HR files, and workflow updates before relying on them. <br>
Risk: Project, learning, and HR files can accumulate sensitive personal or business information. <br>
Mitigation: Keep secrets and sensitive personal or business data out of these files, and review diffs before sharing or publishing outputs. <br>
Risk: The optional daily cron can introduce recurring main-session checks. <br>
Mitigation: Enable the cron only when recurring checks are intended and document how to disable or remove the scheduled task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raydoomed/nephesh-studio) <br>
- [Publisher profile](https://clawhub.ai/user/raydoomed) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Standard workflow](artifact/workflow.md) <br>
- [Subagent scheduling rules](artifact/SUBAGENT-SCHEDULING.md) <br>
- [Daily checklist](artifact/daily-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file templates, workflow instructions, JSON examples, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates project documentation, role knowledge files, QA reports, retrospectives, and optional cron configuration guidance.] <br>

## Skill Version(s): <br>
6.0.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
