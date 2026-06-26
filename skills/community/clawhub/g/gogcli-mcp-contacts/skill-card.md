## Description: <br>
Looks up, searches, and manages Google Contacts and broader Google People API profiles through the gogcli Contacts MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure an MCP-backed assistant for Google Contacts and Workspace directory lookups, including contact search, profile retrieval, and manager or reports relations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can involve sensitive Google Workspace and Contacts access. <br>
Mitigation: Install only when the publisher is trusted with Google Workspace access and review enabled scopes with `google-workspace config show`. <br>
Risk: Write-capable Workspace actions can modify data if enabled. <br>
Mitigation: Keep Docs, Sheets, Drive, and other write modes off unless needed, and avoid Drive readwrite unless broad Drive-file token access is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/gogcli-mcp-contacts) <br>
- [gogcli dependency](https://github.com/openclaw/gogcli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON configuration blocks and inline command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP server configuration and Google Workspace tool-use guidance.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
