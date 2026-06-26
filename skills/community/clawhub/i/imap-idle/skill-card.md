## Description: <br>
Event-driven email monitoring using IMAP IDLE that replaces polling with OpenClaw webhook notifications for multiple IMAP accounts while using no tokens while waiting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[topitip](https://clawhub.ai/user/topitip) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to replace polling-based email checks with IMAP IDLE monitoring that wakes OpenClaw through a configured webhook when new mail arrives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles mailbox credentials for configured IMAP accounts. <br>
Mitigation: Prefer system keyring storage, restrict any config file containing secrets with chmod 600, and use secrets management for container deployments. <br>
Risk: The skill forwards sender, subject, and short body-preview text to the configured webhook. <br>
Mitigation: Keep the webhook local or otherwise trusted, and ensure OpenClaw treats email contents as untrusted input. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/topitip/imap-idle) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Security guide](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides local listener setup and operation; generated configuration and logs are controlled by the user.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and changelog, released 2026-02-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
