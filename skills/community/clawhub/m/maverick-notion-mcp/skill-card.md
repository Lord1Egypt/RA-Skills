## Description: <br>
Search, read, and update Notion pages, databases, blocks, comments, and workspace content via Notion's hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent search, read, and update Notion workspace content through the user's OAuth-granted Notion access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update Notion content using the connected user's OAuth grant. <br>
Mitigation: Confirm the exact Notion page, database, block, comment, or workspace object before any write action. <br>
Risk: Tool arguments and results are sent to Notion's hosted MCP server. <br>
Mitigation: Avoid sending unrelated sensitive data through Notion tool arguments and revoke the Notion OAuth grant when access is no longer needed. <br>


## Reference(s): <br>
- [Notion MCP overview](https://developers.notion.com/guides/mcp/overview) <br>
- [mcporter config docs](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Notion MCP tools and return structured JSON when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
