## Description:

Provides Chinese-language troubleshooting guidance for common OpenClaw installation, connection, model, runtime, database, and configuration issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operations staff use this skill to diagnose common setup, connectivity, model, runtime, database, and configuration failures and receive checklist-style guidance with example commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags high-impact repair commands, including sudo ownership changes, persistent npm registry changes, forced process termination, and OpenClaw reset commands.

Mitigation: Review each command before use, prefer user-scoped or temporary alternatives where possible, create verified backups before reset operations, and define explicit rollback steps.

Risk: The skill includes commands that use bot tokens or API keys in curl examples.

Mitigation: Use placeholders or environment variables for secrets, avoid exposing credentials in shell history or logs, and rotate any token that may have been pasted into a shared terminal.

Risk: The artifact advertises third-party remote support contact paths and paid support tiers.

Mitigation: Verify the support provider independently and avoid sharing credentials, private logs, or production access unless an approved support process is in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-troubleshoot-cn)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw Discord community](https://discord.gg/clawd)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and troubleshooting checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language troubleshooting guidance; commands should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
