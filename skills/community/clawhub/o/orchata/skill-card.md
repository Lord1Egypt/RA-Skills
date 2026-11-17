## Description:

Knowledge management and RAG platform with tree-based document indexing. Use this skill to search, browse, and manage Orchata knowledge bases via MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ehudsn](https://clawhub.ai/user/ehudsn)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to search, browse, upload, update, and organize documents in Orchata knowledge bases through MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented space and document deletion tools can remove knowledge-base content when used with the wrong identifier.

Mitigation: Confirm the exact space or document ID with the user before delete actions, prefer archival where available, and scope MCP credentials to the intended knowledge bases.

Risk: Agents may query documents that are still pending, processing, failed, or otherwise unavailable, leading to empty or incomplete results.

Mitigation: Check document status and query only completed documents before relying on search or retrieval results.

## Reference(s):

- [Orchata Skill Release](https://clawhub.ai/ehudsn/skills/orchata)
- [ehudsn Publisher Profile](https://clawhub.ai/user/ehudsn)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with MCP tool-call examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create, update, search, retrieve, archive, or delete Orchata spaces and documents when authorized.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
