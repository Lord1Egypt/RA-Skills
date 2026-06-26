## Description: <br>
Soft human-in-the-loop approval gate. Asks the user for confirmation before the agent executes high-risk actions like deleting files, sending emails, or running destructive commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openauthority](https://clawhub.ai/user/openauthority) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill during interactive agent sessions to require a conversational approval prompt before high-risk actions such as file deletion, external communication, destructive shell commands, database changes, or financial operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a soft approval reminder rather than a security boundary, so prompt injection, tight loops, context loss, or `/human-approval off` can bypass it. <br>
Mitigation: Use it for interactive visibility only; require a hard enforcement plugin or platform policy for unattended or production approval controls. <br>
Risk: A user may still approve a destructive, external, or financial action without fully understanding the impact. <br>
Mitigation: Review the prompt's action, target, risk, and reversibility fields before approval, and choose modify or reject when the impact is unclear. <br>


## Reference(s): <br>
- [Human Approval on ClawHub](https://clawhub.ai/openauthority/human-approval) <br>
- [OpenAuthority plugin](https://github.com/Firma-AI/openauthority) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown conversation prompts and command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Approval prompts include the action, target, risk, reversibility, and approve/reject/modify options.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
