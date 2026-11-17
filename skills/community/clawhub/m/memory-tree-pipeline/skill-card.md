## Description:

Three-scope structured memory for AI agents that automatically organizes, summarizes, and indexes agent memory with sealing workers and topic extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larios613-hub](https://clawhub.ai/user/larios613-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to give an agent persistent, searchable memory organized into source, topic, and global scopes. It supports storing new memory entries, recalling relevant context, sealing raw entries into summaries, migrating flat memory files, and checking index status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored content can be promoted into persistent reusable agent memory, including sensitive or untrusted content.

Mitigation: Use a dedicated memory workspace and avoid storing secrets, credentials, or untrusted web and tool output unless it is acceptable for that content to become persistent context.

Risk: The forget operation is reported to have an unvalidated path that can delete markdown outside its topic folder.

Mitigation: Constrain or fix the forget operation before automatic agent use, and require review or keep-source behavior for deletion workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/larios613-hub/skills/memory-tree-pipeline)
- [Publisher profile](https://clawhub.ai/user/larios613-hub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown memory files plus plain-text or JSON-like search, status, migration, and sealing results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists memory under a configured workspace and updates index metadata for source, topic, and global scopes.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
