## Description: <br>
Agentic framework for operating monday.com workspaces via the Monday MCP connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharoonsharif](https://clawhub.ai/user/sharoonsharif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to operate monday.com boards, items, groups, columns, forms, updates, and project workflows through a connected monday.com account. It supports project setup, sprint summaries, triage, bulk status updates, and other workspace operations that require board schema discovery before changes are made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad changes in a user's real monday.com workspace, including bulk updates and destructive operations. <br>
Mitigation: Explicitly name the target board or workspace, preview planned changes, and require user confirmation before bulk changes or deletions. <br>
Risk: Dynamic GraphQL calls and integrations with Gmail, Google Calendar, or Fireflies may affect data outside the immediate monday.com task if used without clear boundaries. <br>
Mitigation: Require previews and explicit consent before raw GraphQL calls, transcript imports, calendar event creation, or Gmail draft generation. <br>


## Reference(s): <br>
- [Monday MCP endpoint](https://mcp.monday.com/mcp) <br>
- [Column value formats](references/column-formats.md) <br>
- [Workflow templates](references/workflows.md) <br>
- [ClawHub skill page](https://clawhub.ai/sharoonsharif/monday-ops) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/sharoonsharif) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with structured plans, tables, tool-call guidance, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include monday.com board links, item IDs, column value JSON examples, and progress summaries.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
