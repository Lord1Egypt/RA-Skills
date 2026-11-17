## Description:

Guides safe inspection, configuration, and management of Loboot-owned user services on macOS and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitekiwi](https://clawhub.ai/user/whitekiwi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to preview, manage, and diagnose Loboot-owned per-user services while keeping stored definitions, live runtime, and future activation separate. The Loboot CLI must be installed separately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service changes or enabling future activation can affect the user's current or later sessions.

Mitigation: Review the complete dry-run and obtain authorization for each exact mutation; verify live state afterward.

Risk: Arguments and manifests can expose secrets in plaintext.

Mitigation: Do not put secrets in arguments or manifests; sanitize diagnostic output before sharing.

## Reference(s):

- [Loboot on ClawHub](https://clawhub.ai/whitekiwi/skills/loboot)
- [Loboot installation guide](https://github.com/WhiteKiwi/loboot/blob/main/docs/INSTALL.md)
- [Loboot CLI contract](https://github.com/WhiteKiwi/loboot/blob/main/docs/CLI.md)
- [Loboot operator guide](https://github.com/WhiteKiwi/loboot/blob/main/docs/OPERATOR.md)
- [Loboot safety model](references/safety.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline commands and TOML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates dry-run plans from live observations and flags unknown state.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
