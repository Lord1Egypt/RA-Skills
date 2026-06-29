## Description: <br>
Motion lets an agent operate Motion through an OOMOL-connected account to read, create, update, and delete Motion data using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Motion workspaces, projects, schedules, statuses, users, and tasks through an OOMOL-connected Motion account. It supports read actions plus confirmed creation, update, and deletion workflows for Motion projects and tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can create or modify Motion projects and tasks. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running write actions. <br>
Risk: Destructive task deletion can remove Motion data. <br>
Mitigation: Get explicit approval for the target task before running delete_task. <br>
Risk: The skill requires an OOMOL-connected Motion account and sensitive credentials. <br>
Mitigation: Use OOMOL credential injection and avoid handling raw Motion tokens directly. <br>


## Reference(s): <br>
- [ClawHub Motion Skill](https://clawhub.ai/oomol/oo-motion) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Motion Homepage](https://www.usemotion.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads or results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before payload construction; write and destructive actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
