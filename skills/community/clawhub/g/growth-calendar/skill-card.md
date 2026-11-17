## Description:

Plan, inspect and generate SEO articles on a Timothe Growth Calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timothe](https://clawhub.ai/user/timothe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to inspect a Timothe workspace's SEO content calendar, plan topic clusters, manage scheduled articles and notes, and generate or edit SEO articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend Timothe credits on paid research, cluster planning, and article generation.

Mitigation: Check the workspace credit balance, state the expected cost, and get clear user authorization before calling expensive tools such as plan_cluster or generate_article.

Risk: The skill can change the user's content calendar, including planned article dates, notes, slugs, and deletions.

Mitigation: List the affected items, confirm the intended batch once, and avoid guessing track IDs or dates before making calendar changes.

Risk: Scheduled reservations may generate articles automatically on future dates.

Mitigation: Explain that planned articles can trigger future generation costs and confirm cadence, timezone, market, and article count before scheduling.

Risk: Workspace-wide writing and image style updates affect future generated articles.

Mitigation: Read the current style version first, preserve content that should remain, and apply only the changes the user requested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timothe/skills/growth-calendar)
- [Growth Calendar product page](https://timothe.ai/growth-calendar)
- [Growth Calendar app](https://timothe.ai/tools/growth-calendar/app)
- [Growth Calendar MCP server](https://timothe.ai/mcp/growth-calendar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, links, and MCP tool-use instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide calendar changes, article generation, article edits, style updates, and credit-spending actions in the connected Timothe workspace.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
