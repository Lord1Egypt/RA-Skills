## Description: <br>
Use when the user mentions Jira issues, asks about tickets, wants to create/view/update issues, check sprint status, or manage their Jira workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdrhyne](https://clawhub.ai/user/jdrhyne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, project managers, and support teams use this skill to view, create, update, transition, search, and comment on Jira issues through a conversational agent backed by either the jira CLI or Atlassian MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Jira write actions can create, edit, transition, comment on, link, or bulk-modify tickets. <br>
Mitigation: Review the proposed command or tool call carefully and require explicit approval before executing write actions. <br>
Risk: Jira API tokens or credentials could be exposed if pasted into chat. <br>
Mitigation: Keep Jira credentials in environment variables or the configured backend and avoid pasting tokens into the agent conversation. <br>


## Reference(s): <br>
- [ClawHub JIRA Skill Page](https://clawhub.ai/jdrhyne/jira) <br>
- [Commands Reference](references/commands.md) <br>
- [MCP Reference](references/mcp.md) <br>
- [jira CLI](https://github.com/ankitpokhrel/jira-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, MCP tool calls, tables, and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Jira issue tables, proposed write operations, verification results, and setup guidance when no backend is available.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
