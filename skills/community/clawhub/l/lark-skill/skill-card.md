## Description: <br>
Comprehensive Feishu/Lark integration skill for OpenClaw that covers messaging, group management, Bitable, documents, calendar, video conferencing, meeting minutes, task management, approval workflows, contacts, cloud drive, and wiki operations through the official Lark MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucascheung](https://clawhub.ai/user/lucascheung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and workspace operators use this skill to guide an OpenClaw agent through Feishu/Lark workspace automation, including messages, chats, tables, documents, calendars, meetings, tasks, approvals, contacts, drive files, and wiki pages. It is intended for environments where the official Lark MCP server is configured with an app and scopes controlled by the user or organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad Feishu/Lark workspace read and write actions, including messages, chats, tables, documents, calendars, tasks, approvals, drive files, and wiki pages. <br>
Mitigation: Install it only for a workspace and app you control, use a dedicated Lark app, and grant only the minimum scopes needed for the intended workflow. <br>
Risk: Agent-assisted actions may delete data, change permissions, send important messages, remove participants, access recordings or transcripts, or approve and reject workflows. <br>
Mitigation: Require explicit human review before destructive, permission-changing, communication-sensitive, meeting-recording, transcript, or approval actions. <br>
Risk: Over-broad Lark app scopes increase impact if credentials or agent behavior are misused. <br>
Mitigation: Prefer read-only scopes where possible and keep app credentials limited to the relevant tenant and workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucascheung/lark-skill) <br>
- [Project homepage from ClawHub metadata](https://github.com/lucascheung/lark_skill) <br>
- [Lark Open Platform documentation](https://open.larkoffice.com/document/home/index) <br>
- [Lark Card Builder](https://open.larkoffice.com/cardkit) <br>
- [Official Feishu/Lark OpenAPI MCP server](https://github.com/larksuite/lark-openapi-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of external Lark MCP tools; agent actions depend on configured credentials, tenant permissions, and granted scopes.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata; artifact frontmatter reports 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
