## Description: <br>
GitHub notification auto-triage via an email channel that forwards CI failures and security alerts, buffers PR-related notifications for daily summaries, and silently archives lower-priority notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devincodel](https://clawhub.ai/user/devincodel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill in OpenClaw to route GitHub notification email from a dedicated mailbox into urgent forwards, daily review summaries, or read/archive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub notification content and repository metadata may be forwarded to the resolved master email address. <br>
Mitigation: Review the destination address and forwarded notification fields before installing; use only for repositories and notifications acceptable to expose to that recipient. <br>
Risk: Buffered notification metadata may be stored in workspace memory files visible to local workspace readers. <br>
Mitigation: Review workspace access and retention expectations before use, and avoid private or security-sensitive notifications unless this storage behavior is acceptable. <br>


## Reference(s): <br>
- [GitHub Triage Rules](references/triage-rules.md) <br>
- [ClawHub skill page](https://clawhub.ai/devincodel/github-triage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send email, mark messages read, and write daily buffer JSON files when executed by an agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
