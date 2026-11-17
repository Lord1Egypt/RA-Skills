## Description:

Ultimate memory optimization for AI agents that combines WAL protocol, Working Buffer, three-tier memory, context budgeting, and a learning log system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silaszhu](https://clawhub.ai/user/silaszhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage long OpenClaw sessions by logging active context, preserving decisions and preferences, tiering memories, and creating recovery checkpoints before compaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent workspace memory may store conversation details, preferences, IDs, URLs, and error context in plaintext.

Mitigation: Use the skill only with intentional opt-in, avoid secrets and confidential data, and add redaction plus retention and deletion procedures before use.

Risk: Memory initialization and tiering behavior can create, reset, archive, or overwrite workspace memory files.

Mitigation: Review the affected workspace paths, keep backups, and run initialization or tiering only in workspaces where those file changes are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/silaszhu/skills/proactive-memory-agent)
- [Publisher profile](https://clawhub.ai/user/silaszhu)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated workspace memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify plaintext memory, learning, state, checkpoint, and archive files in the configured OpenClaw workspace.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
