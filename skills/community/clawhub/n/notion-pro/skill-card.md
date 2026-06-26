## Description: <br>
Complete Notion API skill with a Python CLI for search, page and database reads, page creation, property updates, block appends, block archiving, auto-pagination, recursive block reads, and rate-limit retry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baixiaodev](https://clawhub.ai/user/baixiaodev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate on Notion workspaces through a dedicated CLI, including discovering pages and databases, reading nested content, querying databases, creating or updating pages, appending blocks, and archiving blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Notion content shared with its integration, including creating pages, updating properties, appending blocks, and archiving blocks. <br>
Mitigation: Use a dedicated least-privilege Notion integration and share only the specific pages or databases required for the task. <br>
Risk: Bulk updates or delete-block operations can change many workspace records or archive content. <br>
Mitigation: Require the agent to inspect targets, present an explicit operation plan, and verify delete-block or bulk update actions before execution. <br>
Risk: A stale environment variable could point the agent at the wrong Notion integration or workspace scope. <br>
Mitigation: Prefer the OpenClaw skill configuration for the API key and review the configured integration before running write operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/baixiaodev/notion-pro) <br>
- [Publisher profile](https://clawhub.ai/user/baixiaodev) <br>
- [Notion integrations](https://www.notion.so/profile/integrations) <br>
- [Notion API documentation](https://developers.notion.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples; CLI command output is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Python standard-library CLI that reads a Notion API key from OpenClaw config or NOTION_API_KEY and sends authenticated requests to the Notion API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
