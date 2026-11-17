## Description:

A practical memory management system for OpenClaw: importance scoring, time-decay cleanup, write triggers, hybrid retrieval, and daily maintenance workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuchang9337-dev](https://clawhub.ai/user/xuchang9337-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to organize persistent agent memory, decide what should be stored, retrieve prior preferences and decisions, and run daily memory cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files and broad recall can retain sensitive or private information longer than intended.

Mitigation: Require explicit confirmation before saving sensitive memories and review the paths the agent is allowed to read and write.

Risk: Scheduled maintenance can modify, archive, or delete memory logs without immediate user review.

Mitigation: Avoid unattended deletion until backups and retention behavior are tested, and migrate valuable content before cleaning old logs.

Risk: OpenClaw configuration and API-key backup examples are secret-adjacent and may copy sensitive configuration into additional files.

Mitigation: Remove the OpenClaw config and API-key backup commands before enabling cron or copying the examples into an active environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuchang9337-dev/skills/memory-management-lite)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory layout rules, write and recall procedures, daily maintenance steps, and cron configuration examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
