## Description: <br>
Writing Style Skill is a reusable writing-style template that helps an agent draft in a user's style and learn from original-to-final edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzocb](https://clawhub.ai/user/jzocb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and writers use this skill to customize an agent's writing voice, record draft-to-final edits, and generate proposed style-rule improvements for future writing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The observation workflow can store full draft and final text in local JSONL logs. <br>
Mitigation: Avoid recording confidential drafts and periodically inspect or remove local observation logs. <br>
Risk: The improvement workflow can use external LLM output to propose or automatically apply changes to skill instructions. <br>
Mitigation: Review proposal files and SKILL.md diffs before applying changes, and avoid cron or auto mode until the workflow is trusted. <br>
Risk: A custom LLM command can be executed through IMPROVE_LLM_CMD. <br>
Mitigation: Set IMPROVE_LLM_CMD only to a command you control and understand. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jzocb/jz-writing-style-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jzocb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated proposal files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSONL observation logs, Markdown proposal files, and SKILL.md backups when its helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
