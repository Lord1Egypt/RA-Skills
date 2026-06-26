## Description: <br>
Notion integration for OpenClaw. Manage pages, databases, and blocks via AI agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChloePark85](https://clawhub.ai/user/ChloePark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let agents manage Notion workspaces through CLI commands for pages, databases, blocks, and search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or archive Notion workspace content. <br>
Mitigation: Use a dedicated least-privilege Notion integration shared only with the pages or databases needed, and require explicit user confirmation before archive or delete actions. <br>
Risk: The NOTION_TOKEN credential can expose workspace access if logged or shared. <br>
Mitigation: Keep NOTION_TOKEN out of logs and shell history, and rotate the token if exposure is suspected. <br>
Risk: The setup documentation includes a remote uv install command. <br>
Mitigation: Install uv through a trusted package manager or a verified installer instead of piping remote installer output directly to sh. <br>


## Reference(s): <br>
- [Notion API Reference](https://developers.notion.com/reference/intro) <br>
- [Notion Integrations](https://www.notion.so/my-integrations) <br>
- [ClawHub Skill Page](https://clawhub.ai/ChloePark85/notion-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses NOTION_TOKEN and uv; operations return Notion API response JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
