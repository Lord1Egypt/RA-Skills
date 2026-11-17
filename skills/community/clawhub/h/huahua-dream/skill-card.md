## Description:

Huahua Dream helps an agent periodically organize conversation memory, prune stale entries, and write self-reflection notes for long-term continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiye1997](https://clawhub.ai/user/baiye1997)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure a recurring memory-maintenance workflow that reviews session history, updates long-term memory files, and produces concise dream/self-reflection reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring access to private conversation logs.

Mitigation: Enable the skill only for intended workspaces and verify dream-config.json points to the intended agent session path before scheduling cron.

Risk: Persistent long-term memory files can be changed during unattended runs.

Mitigation: Keep MEMORY.md backups, review proposed memory changes, and prefer explicit opt-in or manual review instead of autoApprove.

Risk: Session discovery may select an unintended agent or workspace.

Mitigation: Inspect and correct dream-config.json after setup, including workspace, sessionsPath, timezone, and memory paths.

## Reference(s):

- [Memory Types Classification Guide](references/memory-types.md)
- [Huahua Dream ClawHub Page](https://clawhub.ai/baiye1997/skills/huahua-dream)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON status or configuration output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update memory files, dream records, backups, proposed memory changes, and configuration files.]

## Skill Version(s):

1.1.8 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
