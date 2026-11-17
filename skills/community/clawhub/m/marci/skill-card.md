## Description:

Work with the person's Marci apps (to-dos, trackers, notes, budgets, plans, shared spaces, games and puzzles) through the Marci MCP server at https://mcp.getmarci.ai/mcp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marci](https://clawhub.ai/user/marci)

### License/Terms of Use:

MIT No Attribution

## Use Case:

People using an AI agent can use Marci to manage personal and work records through connected apps, including lists, trackers, plans, shared spaces, reminders, games, and puzzles. The agent can search and update existing apps, help find apps, and open an app when requested, subject to the person's granted access and confirmation rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal conversation details could be saved online without a clear request to store them.

Mitigation: Before granting write access, specify what information may be saved and require confirmation for other personal disclosures. Limit access to the apps needed, and keep medication, symptom, and other sensitive health details out of this integration.

Risk: The remote service implementation was not available for inspection.

Mitigation: Grant access only to the Marci apps needed for the task and review what the agent saves.

## Reference(s):

- [Marci](https://getmarci.ai)
- [Marci MCP server](https://mcp.getmarci.ai/mcp)
- [Marci app ideas](https://getmarci.ai/.well-known/agent-skills/marci/references/ideas.md)
- [Marci on ClawHub](https://clawhub.ai/marci/skills/marci)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration instructions, Shell commands, Text, Markdown]

**Output Format:** [Markdown guidance with tool calls and configuration or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summaries of records read or written in connected Marci apps.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
