## Description:

Protects OpenClaw's openclaw.json with automatic rollback, lock mode, multi-version baseline snapshots, audit logging, and SIGUSR1 gateway hot-reload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbcvv](https://clawhub.ai/user/xbcvv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and OpenClaw operators use this skill to install and operate a root-level systemd guardian for OpenClaw configuration recovery, auditability, and gateway reload after validated changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent root service can overwrite openclaw.json and signal the gateway process.

Mitigation: Install only after administrator review, confirm the service scope is acceptable, and test rollback and reload behavior in a controlled environment before production use.

Risk: Security-event details may be sent through hard-coded Discord and Telegram alert targets.

Mitigation: Disable external alerts or replace the alert targets with administrator-controlled destinations before enabling the service.

Risk: Configuration validation may rely on matching the text "Config valid" rather than the validator exit status.

Mitigation: Update validation to trust the validator exit code before depending on automatic rollback for safety-critical recovery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xbcvv/skills/openclaw-config-guardian)
- [Publisher profile](https://clawhub.ai/user/xbcvv)
- [Architecture design](artifact/references/DESIGN.md)
- [Usage guide](artifact/references/USAGE.md)
- [Operations guide](artifact/references/OPERATION.md)
- [Archive index](artifact/references/ARCHIVE.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and operational configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation, operation, recovery, and troubleshooting guidance for a Linux systemd service.]

## Skill Version(s):

1.0.4 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
