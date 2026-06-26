## Description: <br>
Use Notion through mcporter-backed MCP tools. Use when working with Notion pages, databases, search, content updates, or workspace lookups via an MCP-integrated Notion server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dam1k](https://clawhub.ai/user/dam1k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search, read, and update Notion pages and databases through a configured MCP-integrated Notion server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured MCP or Notion server can access workspace content using the user's Notion credentials. <br>
Mitigation: Install only when the configured server is trusted, use a least-privilege Notion integration token, and grant access only to required pages or databases. <br>
Risk: Credential values could be exposed if placed in prompts or committed files. <br>
Mitigation: Load the Notion token from the runtime environment, normally as NOTION_TOKEN, and keep credentials out of prompts and repositories. <br>
Risk: Broad write operations could update unintended Notion pages or databases. <br>
Mitigation: Inspect the target page or database before writes, keep changes narrow, and review proposed updates before broad workspace changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dam1k/notion-remote-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Notion MCP tool calls and scoped workspace updates for user review.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
