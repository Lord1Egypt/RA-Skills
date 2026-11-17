## Description:

Plan to Eat CLI lets an agent manage Plan to Eat meal plans, recipes, planner notes and ingredients, freezer entries, and shopping lists through the plan-to-eat shell command when MCP tools are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-zwingli](https://clawhub.ai/user/alex-zwingli)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users with Plan to Eat accounts use this skill to inspect and update meal plans, recipes, planner notes, freezer entries, and shopping lists from a shell when the MCP server is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can read and modify a user's Plan to Eat account, including planner, freezer, and shopping-list data.

Mitigation: Install only when account access is acceptable, review planned write operations with the user, and confirm destructive changes before execution.

Risk: The skill requires Plan to Eat credentials.

Mitigation: Use environment variables or a local .env file, and do not ask users to paste passwords into chat or inline credentials in shell commands.

Risk: Running an unpinned npm install or npx command can fetch a future package version.

Mitigation: Keep npm package versions pinned and prefer an already installed or otherwise verified CLI before running account-affecting commands.

Risk: Meal titles, notes, and shopping-list text may contain shell-sensitive characters.

Mitigation: Pass user text as quoted command arguments or data values such as jq --arg rather than interpolating it into command strings.

## Reference(s):

- [Project homepage](https://github.com/alex-zwingli/plan-to-eat-mcp)
- [Plan to Eat CLI command reference](https://github.com/alex-zwingli/plan-to-eat-mcp/blob/main/docs/TOOLS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should request JSON output where available, keep npm package versions pinned, and treat account writes as immediate.]

## Skill Version(s):

0.7.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
