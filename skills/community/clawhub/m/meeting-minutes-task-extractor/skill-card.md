## Description: <br>
Free basic version that extracts actionable tasks from meeting minutes and reserves premium upgrade hooks for deeper action decomposition and project tracker export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wingogx](https://clawhub.ai/user/wingogx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and productivity-focused users can use this skill to turn meeting notes into a small structured task list with assignee, due-date, and priority hints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill output can include a paid-upgrade link containing the supplied user_id. <br>
Mitigation: Treat payment links as untrusted unless the destination is recognized, and review the configured payment URL before use. <br>
Risk: Meeting notes may contain sensitive business or personal information. <br>
Mitigation: Use the skill only with notes you are comfortable sharing with the local skill publisher's code and review inputs before execution. <br>


## Reference(s): <br>
- [SkillPay API Contract](references/skillpay-api-contract.md) <br>
- [ClawHub skill page](https://clawhub.ai/wingogx/meeting-minutes-task-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON object printed by a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 5 free-tier tasks with assignee, due-date, and priority fields, plus an upgrade object.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
