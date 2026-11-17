## Description:

Search and retrieve relevant information from indexed memory files using semantic queries and direct file reads for context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aigentic-net](https://clawhub.ai/user/aigentic-net)

### License/Terms of Use:


## Use Case:

Agents use this skill to check remembered conversations, preferences, dates, project history, todos, and other personal context before answering questions that depend on prior interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retrieve personal stored context from memory files, daily notes, raw logs, and enabled transcripts.

Mitigation: Enable it only where that access is acceptable, and avoid transcript indexing for highly sensitive chats.

Risk: Search snippets can omit surrounding context or fail to find relevant memories.

Mitigation: Use direct memory reads for promising results and state when a memory search finds no supporting information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aigentic-net/skills/memory-search)
- [Publisher profile](https://clawhub.ai/user/aigentic-net)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown guidance with JSON tool-call examples and structured memory search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include snippets, relative paths, line ranges, relevance scores, and citations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
