## Description:

MemPalace provides persistent semantic memory management for searching, adding, and querying memories stored in a ChromaDB-backed palace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderotxoa](https://clawhub.ai/user/anderotxoa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain local persistent memory, retrieve semantically similar stored content, inspect palace status, and query knowledge graph facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored memories may include sensitive or proprietary content that is retained locally over time.

Mitigation: Use this skill only when persistent local retention is intended, and avoid storing secrets, credentials, private user data, or proprietary material unless retention is approved.

Risk: Search, diary, and knowledge graph results may surface verbatim stored content.

Mitigation: Review retrieved results before sharing or reusing them outside the local agent workflow.

## Reference(s):

- [MemPalace MCP Tools Reference](references/mcp_tools.md)
- [ClawHub Skill Page](https://clawhub.ai/anderotxoa/skills/mempalace-ander)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts read and write local ChromaDB-backed memory at the configured palace path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
