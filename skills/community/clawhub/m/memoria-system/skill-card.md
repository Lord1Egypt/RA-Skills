## Description:

Manages AI assistant long-term memory with layered storage for facts, events, skills, active context, and indexes, including backup, rollback, migration, and health-check tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuilinshen](https://clawhub.ai/user/cuilinshen)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI assistant operators use this skill to initialize and maintain a local, layered memory directory for facts, conversations, workflows, active context, and search indexes. It also provides shell tools for backup, rollback, migration, and integrity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup and rollback scripts can delete or overwrite broad filesystem paths if configuration or backup names are wrong or abused.

Mitigation: Keep memory and backup paths under a dedicated directory, avoid elevated execution, review rollback targets before use, and avoid unattended --fix until the writes are understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cuilinshen/skills/memoria-system)
- [Artifact README](artifact/README.md)
- [Artifact SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Bash commands, JSON configuration, and filesystem templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and manages local memory files, backup archives, migration state, and health-check reports.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
