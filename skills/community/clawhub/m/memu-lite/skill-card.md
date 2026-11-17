## Description:

memU-lite is a lightweight structured memory system for OpenClaw that stores atomic Markdown memories by category, maintains tag indexes, and provides shell tools for adding, searching, backing up, tagging, and cleaning memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoo-unison](https://clawhub.ai/user/yoo-unison)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent operators use memU-lite to create and maintain local long-term memory for OpenClaw agents, including preferences, knowledge, relationships, tasks, and reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates durable local agent memory that may persist across future sessions.

Mitigation: Review stored memories regularly, avoid saving secrets or sensitive personal data, and isolate or remove sample memories before relying on the workspace.

Risk: Backup restore behavior can overwrite the current local memory directory.

Mitigation: Inspect backup archives before restoration and restore only archives from trusted sources after confirming the current memory state is backed up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoo-unison/skills/memu-lite)
- [memU reference project](https://github.com/NevaMind-AI/memU)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shell tools can create, search, back up, restore, tag, archive, or delete local memory files under ~/.openclaw/workspace/memory.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
