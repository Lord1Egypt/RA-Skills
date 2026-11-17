## Description:

理财小助手 helps users record income and expenses, review balances and statistics, generate weekly spending reports, set monthly budgets, and receive overspending alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[786793119](https://clawhub.ai/user/786793119)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill as a personal finance assistant to record income and expenses, inspect current balance and spending statistics, generate weekly reports, and manage monthly budget alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal finance records and budget data are stored locally in JSON files under ~/.memory/finance.

Mitigation: Confirm local storage is acceptable for the user and protect or exclude that directory according to local privacy and backup policies.

Risk: The artifact references a Python script that was not included in the inspected artifact.

Mitigation: Run the referenced script only if it comes from a trusted source and has been reviewed before execution.

## Reference(s):

- [ClawHub skill page: pocket-money-manager](https://clawhub.ai/786793119/skills/pocket-money-manager)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes local JSON storage under ~/.memory/finance for finance records and budget settings.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
