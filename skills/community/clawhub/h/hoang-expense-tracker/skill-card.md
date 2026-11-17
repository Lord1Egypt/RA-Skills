## Description:

A Vietnamese personal finance assistant that helps users log expenses, view spending reports and charts, set category budgets, and get playful spending feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoanghust2003](https://clawhub.ai/user/hoanghust2003)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to track day-to-day personal spending in Vietnamese, generate category summaries and pie charts, set simple budgets, and receive lightweight spending advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied expense text may be passed into shell-style command invocations.

Mitigation: Use structured argument passing with validation and explicit confirmation before executing expense commands.

Risk: Spending records and generated report images are stored locally in plaintext.

Mitigation: Store only data the user intends to keep locally, restrict file access, and delete exported CSV or PNG files when they are no longer needed.

Risk: The security verdict is suspicious and recommends review before installation.

Mitigation: Review the skill and scanner guidance before deployment, and limit use to deliberate Vietnamese expense-tracking workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hoanghust2003/skills/hoang-expense-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration]

**Output Format:** [JSON tool output summarized in conversational Markdown; report workflows may also produce a local PNG chart and CSV expense records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local plaintext expense data to expenses.csv and report charts to expense_chart.png.]

## Skill Version(s):

1.0.0 (source: server release evidence, released 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
