## Description:

Stores and manages complete conversation history with searchable local storage, chunked and daily summaries, and automatic syncing of key decisions to MEMORY.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louch84](https://clawhub.ai/user/louch84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to preserve full conversation history, search prior sessions, recall summarized topics, and keep selected long-term decisions available across OpenClaw workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full conversation history may include secrets, personal data, customer data, or sensitive business context.

Mitigation: Use only in workspaces where persistent local retention is acceptable, protect the database and MEMORY.md files, and periodically review or purge stored content.

Risk: Automatically captured decisions may write incorrect or unintended memories into MEMORY.md.

Mitigation: Review MEMORY.md after sync or compaction runs, remove unsuitable entries, and require human review before relying on captured decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/louch84/skills/memory-lcm)
- [Publisher profile](https://clawhub.ai/user/louch84)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript examples, and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and retrieves session-scoped memory, search results, summaries, and MEMORY.md entries.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
