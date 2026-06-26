## Description: <br>
Checks remaining MiniMax API token quota and provides guidance for scheduled monitoring with optional Telegram notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SherLockfate](https://clawhub.ai/user/SherLockfate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check MiniMax API token quota, configure scheduled quota monitoring, and set up low-balance Telegram alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MiniMax API keys and optional Telegram credentials may expose quota status, bot identifiers, chat identifiers, or notification timing if handled carelessly. <br>
Mitigation: Provide credentials through environment variables or a secret manager, restrict Telegram recipients, and review the alert configuration before enabling notifications. <br>
Risk: The submitted artifact describes a Python checker and systemd service, but those implementation files are not included in the package. <br>
Mitigation: Review and scan any separate script or service file before running quota checks, starting monitors, or installing a systemd service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SherLockfate/minimax-token) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax API key; Telegram bot token and chat ID are optional for notifications.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
