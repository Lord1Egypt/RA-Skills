## Description:

Guides agents to build NocoBase pages, including menus, tables, forms, popups, KPIs, JavaScript blocks, outlines, and event flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexander-lq](https://clawhub.ai/user/alexander-lq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create and maintain NocoBase page structures from user requests. It supports CRUD pages, menus, layouts, filters, tables, forms, detail popups, KPI blocks, JavaScript blocks, outlines, event flows, and inspection or debugging commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to change NocoBase UI structure through page, menu, layout, field, column, JavaScript, and event-flow tools.

Mitigation: Install it only for agents that are expected to build or maintain NocoBase pages, and scope activation to NocoBase page-building requests.

Risk: Some supported tools can delete routes, clean or rebuild layouts, remove fields or columns, or add JavaScript and event-flow behavior.

Mitigation: Require explicit user confirmation before destructive changes or before adding JavaScript and event-flow behavior.

Risk: Broad page-building triggers may activate the skill for generic page or form requests.

Mitigation: Narrow triggers or routing rules so the skill is selected only for NocoBase-specific page-building work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexander-lq/skills/pagesskill)
- [Publisher profile](https://clawhub.ai/user/alexander-lq)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline tool-call examples and JSON or JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to guide NocoBase page-building tool calls and related page configuration.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
