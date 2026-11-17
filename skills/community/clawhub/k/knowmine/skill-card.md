## Description:

Save and search personal notes, decisions, and insights with semantic search via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiing99](https://clawhub.ai/user/yiing99)

### License/Terms of Use:

MIT-0

## Use Case:

External users and AI-agent developers use KnowMine to give an agent a remote personal knowledge base for saving, updating, retrieving, and analyzing notes, decisions, memories, and insights across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected notes, memories, and profile-like summaries are sent to KnowMine for remote storage and semantic search.

Mitigation: Use the skill only for content appropriate for a cloud personal-knowledge service, and avoid saving secrets, credentials, regulated data, or highly sensitive personal information.

Risk: Installing with an unpinned @latest installer can pull a newer release than the one reviewed here.

Mitigation: Prefer a pinned installer version when available and review release evidence before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yiing99/skills/knowmine)
- [KnowMine website](https://knowmine.ai)
- [KnowMine MCP settings](https://knowmine.ai/settings/mcp)
- [KnowMine MCP endpoint](https://knowmine.ai/api/mcp)
- [KnowMine MCP health check](https://knowmine.ai/api/mcp/health)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [MCP tool responses containing saved knowledge, search results, memories, profile summaries, and insight summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a KnowMine API key and sends selected knowledge content to the KnowMine remote service.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
