## Description:

Semantic search for Obsidian notes using AI vector embeddings. Find notes by meaning, discover connections, filter by tags/dates/folders, and retrieve full content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent search, list, retrieve, and analyze connections across an Obsidian vault that has been synced to Obvec.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access and display full note contents from a third-party Obvec index.

Mitigation: Install only if comfortable syncing the Obsidian vault to Obvec, and ask the agent to confirm before opening full note bodies for ambiguous requests.

Risk: The MCP URL contains an embedded authentication token.

Mitigation: Treat the MCP URL as a password and regenerate it if exposed.

## Reference(s):

- [Obvec](https://obsidian.10xboost.org/)
- [ClawHub Skill Page](https://clawhub.ai/snoopyrain/skills/obsidian-search)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries with note titles, excerpts, full note content, similarity scores, and ranked related-note lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only retrieval; can display full note contents from the connected Obsidian vault.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
