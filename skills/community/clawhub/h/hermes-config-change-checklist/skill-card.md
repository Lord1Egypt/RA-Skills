## Description:

Use when changing, reviewing, or troubleshooting Hermes Agent settings; the checklist guides discovery, safe edits, verification, and restart reporting across configuration and skill maintenance tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinian5216](https://clawhub.ai/user/xinian5216)

### License/Terms of Use:

MIT-0

## Use Case:

Hermes Agent operators and developers use this checklist to plan configuration changes, verify affected systems, protect secrets and profiles, and report whether a gateway restart is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification may make billable provider calls or start configured MCP servers.

Mitigation: Confirm the target profile and intended changes, and account for provider cost and MCP startup before running verification.

Risk: Bulk maintenance could remove useful skills or rewrite configuration too broadly.

Mitigation: Review deletion candidates and keep backups before bulk changes.

## Reference(s):

- [Skill library maintenance guide](references/skill-library-maintenance.md)
- [ClawHub release page](https://clawhub.ai/xinian5216/skills/hermes-config-change-checklist)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown checklist and structured report with inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
