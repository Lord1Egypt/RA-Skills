## Description: <br>
Comprehensive Feishu/Lark integration skill for OpenClaw covering messaging, group management, Bitable tables, documents, calendar, video conferencing, meeting minutes, task management, approvals, contacts, cloud drive, and wiki workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucascheung](https://clawhub.ai/user/lucascheung) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workplace automation users use this skill to let an agent work with Feishu/Lark collaboration surfaces such as messages, groups, documents, calendars, tasks, approvals, meeting records, and knowledge bases through the configured Lark MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive workplace data from chats, documents, calendars, contacts, meeting recordings, transcripts, approvals, and cloud drive content. <br>
Mitigation: Use the narrowest Lark app scopes possible, limit account access, and review retrieved content before sharing it outside the intended audience. <br>
Risk: The skill documents destructive or high-impact actions such as deleting messages, records, files, tasks, groups, calendar events, reservations, and changing permissions or approval states. <br>
Mitigation: Require explicit user confirmation before deletion, permission changes, approval decisions, removing people, ending meetings, or other irreversible workplace actions. <br>
Risk: The security verdict is suspicious because the integration is broad and the artifact does not provide enough safety guidance for sensitive Lark operations. <br>
Mitigation: Review the skill before installing and constrain it to non-admin credentials unless elevated access is required for a specific workflow. <br>


## Reference(s): <br>
- [ClawHub Lark Skill Page](https://clawhub.ai/lucascheung/lark-mcp) <br>
- [Lark MCP Homepage](https://github.com/lucascheung/lark-mcp) <br>
- [Official Lark OpenAPI MCP Server](https://github.com/larksuite/lark-openapi-mcp) <br>
- [Lark Open Platform Documentation](https://open.larkoffice.com/document/home/index) <br>
- [Lark Card Builder](https://open.larkoffice.com/cardkit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, Shell commands, API calls, Markdown] <br>
**Output Format:** [Markdown guidance with YAML examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Lark MCP server and LARK_APP_ID/LARK_APP_SECRET credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter lists documentation version 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
