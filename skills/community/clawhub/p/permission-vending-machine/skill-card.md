## Description: <br>
Permission Vending Machine gates sensitive AI-agent operations behind human-approved, time-limited grants delivered through messaging, email, chat, or HTTP approval channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tylerdotai](https://clawhub.ai/user/tylerdotai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to require human approval before an AI agent deletes files, force-pushes git history, moves files to trash, or performs similar destructive operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approval paths can authorize destructive actions when request binding is weak or approval tokens are exposed. <br>
Mitigation: Bind the HTTP server to localhost or a protected network and require valid tokens tied to a single pending request and approver. <br>
Risk: GET approval links can be forwarded, logged, or opened unintentionally before a destructive action. <br>
Mitigation: Avoid GET approval links for real destructive actions and prefer protected approval flows with explicit confirmation. <br>
Risk: Logs, the SQLite database, and notification-channel credentials can expose approval context or secrets. <br>
Mitigation: Protect or redact logs and the database, and use dedicated revocable credentials for email, Discord, Telegram, Slack, or Sendblue. <br>


## Reference(s): <br>
- [Permission Vending Machine ClawHub Page](https://clawhub.ai/tylerdotai/permission-vending-machine) <br>
- [README.md](artifact/README.md) <br>
- [Architecture](artifact/docs/ARCHITECTURE.md) <br>
- [Platform-Specific Setup](artifact/docs/PLATFORMS.md) <br>
- [Permission Guard Skill](artifact/skills/permission-guard/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Permission requests can create time-limited grants and audit-log entries after human approval.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
