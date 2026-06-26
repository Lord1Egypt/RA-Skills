## Description: <br>
Notion MCP provides managed-authentication access to Notion workspaces for querying databases, creating and updating pages, managing blocks, comments, teams, users, and related workspace content via Maton. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect an agent to a Notion workspace through Maton-managed MCP authentication. It supports workspace search, content retrieval, page and database creation, page updates, moves, duplication, comments, teams, and user lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and can broker access to connected Notion workspace content. <br>
Mitigation: Keep MATON_API_KEY secret, install only if Maton is trusted, and verify the active workspace or connection before use. <br>
Risk: Write-capable operations can create, update, move, duplicate, comment on, or otherwise change Notion content. <br>
Mitigation: Require explicit confirmation of the target resource and intended effect before approving any write operation. <br>
Risk: Accounts with multiple Notion connections could route requests to the wrong workspace. <br>
Mitigation: Use the Maton-Connection header or otherwise verify the intended connection before sending requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/notion-mcp) <br>
- [Maton](https://maton.ai) <br>
- [Notion MCP Overview](https://developers.notion.com/guides/mcp) <br>
- [MCP Supported Tools](https://developers.notion.com/guides/mcp/mcp-supported-tools) <br>
- [notion-search schema](schemas/notion-search.json) <br>
- [notion-fetch schema](schemas/notion-fetch.json) <br>
- [notion-create-pages schema](schemas/notion-create-pages.json) <br>
- [notion-update-page schema](schemas/notion-update-page.json) <br>
- [notion-create-database schema](schemas/notion-create-database.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and Python or JavaScript request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Notion MCP workspace through Maton.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
