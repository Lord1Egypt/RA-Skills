## Description: <br>
Knowledge management and RAG platform with tree-based document indexing. Use this skill to search, browse, and manage Orchata knowledge bases via MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ehudsn](https://clawhub.ai/user/ehudsn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge-work teams use this skill to search, browse, and manage Orchata knowledge spaces and documents through MCP tools for retrieval-augmented workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can delete spaces or documents, which may remove important business, legal, customer, or operational content. <br>
Mitigation: Require the agent to restate the exact space or document name and ID and get explicit confirmation before any delete action; prefer archiving or backups when available. <br>
Risk: Search results can omit documents that are still pending, processing, failed, inaccessible, or not relevant to the query wording. <br>
Mitigation: Check document status before relying on results and broaden or refine queries when results are empty or incomplete. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose MCP actions that create, update, query, or delete spaces and documents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
