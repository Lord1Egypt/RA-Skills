## Description: <br>
Connect to personal Microsoft accounts via Microsoft Graph API to manage email, calendar events, and tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielithomas](https://clawhub.ai/user/danielithomas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use OfficeClaw to read and manage Outlook mail, calendar events, and Microsoft To Do tasks through Microsoft Graph after one-time OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an agent to a personal Microsoft account and can expose mail, calendar, and task data through Microsoft Graph. <br>
Mitigation: Install only when that account access is intended, prefer read-only mail and calendar scopes where possible, and review the PyPI package before authenticating. <br>
Risk: Email sending and delete operations can modify external account state if enabled. <br>
Mitigation: Keep send and delete disabled unless needed, confirm destructive actions, and configure OFFICECLAW_ALLOWED_RECIPIENTS before enabling email sending. <br>
Risk: Outbound email without an allowlist may send to unintended recipients. <br>
Mitigation: Use OFFICECLAW_ALLOWED_RECIPIENTS to restrict recipients; blocked sends are logged and alert files are written for monitoring. <br>


## Reference(s): <br>
- [OfficeClaw on PyPI](https://pypi.org/project/officeclaw/) <br>
- [Microsoft Graph API](https://docs.microsoft.com/graph/) <br>
- [Microsoft Entra app registration guide](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OfficeClaw on ClawHub](https://clawhub.ai/danielithomas/officeclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports JSON output from officeclaw commands when the --json flag is used.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
