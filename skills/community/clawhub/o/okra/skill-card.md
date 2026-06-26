## Description: <br>
OkraPDF — upload PDFs, read extracted content, ask questions, extract structured data, and manage collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steventsao](https://clawhub.ai/user/steventsao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use OkraPDF to upload PDFs, inspect extracted content, ask document questions, extract structured JSON, manage collections, and script PDF workflows through MCP, CLI, HTTP, or SDK interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded PDFs, prompts, and exports are shared with an external PDF-processing service. <br>
Mitigation: Use OkraPDF only for documents approved for that provider and avoid uploading secrets, regulated records, customer data, or proprietary documents unless the provider and retention policy are approved. <br>
Risk: API keys can be exposed or reused unintentionally in local MCP, CLI, HTTP, or SDK workflows. <br>
Mitigation: Use a dedicated OkraPDF API key, store it in approved secret storage, and rotate it if it appears in logs, shell history, or shared configuration. <br>
Risk: Delete, export, sandbox, and large parallel collection operations can change data access patterns, produce broad exports, or increase service usage. <br>
Mitigation: Require explicit confirmation before running destructive, export, sandbox, or high-volume parallel operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/steventsao/okra) <br>
- [OkraPDF Documentation](https://docs.okrapdf.com) <br>
- [OkraPDF API Reference](https://api.okrapdf.com) <br>
- [OkraPDF MCP Endpoint](https://api.okrapdf.com/mcp) <br>
- [OkraPDF SDK](https://github.com/okrapdf/sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets, shell commands, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include page citations, structured JSON extraction schemas, NDJSON collection query streams, and export commands depending on the workflow] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
