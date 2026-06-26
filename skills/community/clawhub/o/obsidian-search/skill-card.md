## Description: <br>
Semantic search for Obsidian notes using AI vector embeddings, with tools to find notes by meaning, discover connections, filter by tags, dates, and folders, and retrieve full note content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to search and retrieve information from an Obsidian vault through semantic queries, filtered note browsing, full-note retrieval, and related-note analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private Obsidian note content is uploaded to and indexed by the third-party Obvec service as text and vector embeddings. <br>
Mitigation: Sync only vaults whose contents are appropriate for third-party processing, review the provider's deletion controls, and avoid syncing sensitive notes unless that handling is acceptable. <br>
Risk: The MCP server URL contains an embedded token that grants read-only access to search, list, retrieve, and analyze note content. <br>
Mitigation: Treat the MCP URL like a password, keep it out of public logs and shared files, and revoke or regenerate the token if it is exposed. <br>
Risk: Tokens expire after 30 days, which can interrupt note search workflows. <br>
Mitigation: Refresh the MCP link from Obvec settings when the token expires and update the connector configuration. <br>


## Reference(s): <br>
- [Obvec homepage](https://obsidian.10xboost.org/) <br>
- [ClawHub skill page](https://clawhub.ai/snoopyrain/obsidian-search) <br>
- [Publisher profile](https://clawhub.ai/user/snoopyrain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text with note titles, excerpts, relevance scores, full note content, and connection lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only note search and retrieval results depend on the connected Obsidian vault, token validity, and Obvec indexing state.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
