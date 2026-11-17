## Description:

Diagnose and recover from common OpenClaw failures including gateway outages, locked tools, provider errors, routing problems, scheduled job failures, and plugin or skill load failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scsays](https://clawhub.ai/user/scsays)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users, operators, and developers use this skill to triage broken or unhealthy OpenClaw setups and choose recovery commands or configuration changes for common gateway, provider, channel, cron, and plugin failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends broad tool access by setting tools.profile to full.

Mitigation: Review the current security profile before changing it, back up the OpenClaw configuration, and restore the least-privilege profile after recovery.

Risk: The skill recommends direct edits to OpenClaw auth and account-state files.

Mitigation: Back up auth and configuration files before editing them, inspect changes before restart, and rotate affected credentials if auth material may have been exposed or corrupted.

Risk: The artifact promotes an external installer that was not reviewed as part of the skill artifact.

Mitigation: Use the read-only diagnostic guidance first and separately inspect the installer source and behavior before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scsays/skills/openclaw-urgent-care)
- [Claw Mart](https://www.shopclawmart.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
