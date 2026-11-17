## Description:

Safely configures OpenClaw AI model assignments with role validation, backups, rollback, fallback planning, and CLI or dashboard management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frank-bot07](https://clawhub.ai/user/frank-bot07)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to change model assignments, validate model-role compatibility, maintain fallback chains, and recover from unsafe or broken model configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local dashboard exposes unauthenticated credential and configuration-changing APIs while the server is running.

Mitigation: Avoid running the dashboard server unless authentication and trusted-origin checks are added.

Risk: Legacy backup UI or server files may preserve unsafe behavior in installed artifacts.

Mitigation: Remove legacy backup UI and server files from installed artifacts before use.

Risk: .env writes and exposed provider or Telegram tokens can create credential exposure if the server is used with untrusted browser content.

Mitigation: Restrict .env writes to known provider keys and rotate provider or Telegram tokens if the server was run while browsing untrusted sites.

## Reference(s):

- [Model Switchboard ClawHub skill page](https://clawhub.ai/frank-bot07/skills/model-switchboard)
- [Publisher profile](https://clawhub.ai/user/frank-bot07)
- [README](artifact/README.md)
- [Architecture](artifact/ARCHITECTURE.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose OpenClaw model configuration changes, backup and restore actions, validation steps, and dashboard usage.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
