## Description: <br>
Create and manage macro-task pipelines for QA, roadmaps, and feature rollouts using a PIPELINE.md and HEARTBEAT.md pattern for autonomous cron-driven execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[santacruzg282-cyber](https://clawhub.ai/user/santacruzg282-cyber) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure multi-step project work into repository-tracked pipeline steps, heartbeat instructions, verification commands, cron scheduling, and completion commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring autonomous execution can modify and commit repository files without a user present. <br>
Mitigation: Enable the cron workflow only after reviewing every pipeline step, limiting allowed commands and touched files, and confirming how to disable the cron job. <br>
Risk: Discord notifications may expose project status or other repository context without clear privacy scoping. <br>
Mitigation: Remove Discord notification steps or explicitly approve the target channel and notification content before use. <br>
Risk: The HEARTBEAT.md workflow is designed to be locked, which can make remediation harder if instructions need to change. <br>
Mitigation: Confirm the operator knows how to unlock and update HEARTBEAT.md before enabling the workflow. <br>


## Reference(s): <br>
- [Macro Pipeline on ClawHub](https://clawhub.ai/santacruzg282-cyber/macro-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PIPELINE.md and HEARTBEAT.md patterns, cron setup guidance, subagent task templates, status conventions, verification commands, and commit conventions.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
