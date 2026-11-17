## Description:

Use when the user wants to interact with Plan to Eat (plantoeat.com) through the connected plan-to-eat MCP server to view or update meal plans, recipes, planner notes, ingredients, leftovers, freezer entries, and shopping lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-zwingli](https://clawhub.ai/user/alex-zwingli)

### License/Terms of Use:

MIT-0

## Use Case:

External Plan to Eat users and their agents use this skill to operate a connected Plan to Eat MCP server for meal planning, recipe lookup, freezer tracking, and shopping list management. It is intended for accounts whose owner has supplied the required Plan to Eat credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Plan to Eat account credentials and may use a local session file.

Mitigation: Keep credentials in the user's environment, never request passwords in chat, and scope the session file to the user's own machine.

Risk: The connected MCP server can read and write meal plans, recipes, freezer entries, and shopping lists.

Mitigation: Confirm dates, item identifiers, and intended changes before write actions, then re-read account state when confirmation matters.

Risk: Install commands have ordinary supply-chain exposure.

Mitigation: Install only from a trusted package version or repository, prefer the pinned npm command, and verify published artifacts with npm audit signatures when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alex-zwingli/skills/plan-to-eat)
- [Project homepage](https://github.com/alex-zwingli/plan-to-eat-mcp)
- [plan-to-eat-mcp npm package](https://www.npmjs.com/package/plan-to-eat-mcp)
- [Tool reference](https://github.com/alex-zwingli/plan-to-eat-mcp/blob/main/docs/TOOLS.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected plan-to-eat MCP server and user-provided Plan to Eat credentials for live account actions.]

## Skill Version(s):

0.7.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
