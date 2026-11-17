## Description:

Agentic framework for operating monday.com workspaces via the Monday MCP connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharoonsharif](https://clawhub.ai/user/sharoonsharif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to manage monday.com boards, items, groups, columns, status reporting, triage, and project workflows through the Monday MCP connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and change persistent monday.com records, including boards, items, columns, groups, updates, and cross-service actions.

Mitigation: Confirm board visibility, destructive operations, and any Calendar, Gmail, or Fireflies action with the user before execution.

Risk: Workspace data may include confidential, personnel, customer, or launch information.

Mitigation: Review the skill before installation in sensitive workspaces and limit use to data the user is authorized to expose to the connected agent session.

Risk: Broad triggers and workflow automation can lead to unintended workspace changes.

Mitigation: Use the discover, plan, execute pattern and ask for approval before applying multi-step, bulk, destructive, or dynamic GraphQL operations.

## Reference(s):

- [Monday MCP endpoint](https://mcp.monday.com/mcp)
- [Column Value Formats](references/column-formats.md)
- [Workflow Templates](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown with structured tables, summaries, and MCP tool-call plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify persistent monday.com workspace records when the connected tools are used.]

## Skill Version(s):

0.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
