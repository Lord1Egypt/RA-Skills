## Description: <br>
Operate Notion workspace content through Notion MCP using the UXC CLI, including search, fetch, users/teams lookup, page/database creation and updates, and comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to a Notion workspace through Notion MCP and UXC OAuth, then search, fetch, inspect, create, update, and comment on Notion content with read-first and explicit-confirmation guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to request Notion workspace read and write access through OAuth. <br>
Mitigation: Review the Notion OAuth consent screen carefully and approve only the intended workspace and scopes before completing the callback. <br>
Risk: Create, update, move, delete, and comment operations can change Notion workspace content. <br>
Mitigation: Search or fetch current state first, then require explicit user confirmation before any write or destructive action. <br>
Risk: Duplicate endpoint bindings or stale credentials can cause authorization failures. <br>
Mitigation: Verify the matching binding and test explicit credentials before removing stale bindings or retrying the operation. <br>


## Reference(s): <br>
- [Notion-specific auth notes](references/oauth-and-binding.md) <br>
- [Invocation patterns by task](references/usage-patterns.md) <br>
- [Notion-specific failure notes](references/error-handling.md) <br>
- [Notion MCP endpoint](https://mcp.notion.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON envelope parsing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-first workflow with explicit confirmation before create, update, move, delete, or comment actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
