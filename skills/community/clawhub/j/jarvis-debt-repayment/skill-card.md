## Description:

Automates daily income, expense, and debt repayment tracking with local Markdown logs, progress summaries, and recurring finance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesiyoq965-sudo](https://clawhub.ai/user/mesiyoq965-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to help an agent record income, expenses, debt balances, repayment progress, and produce daily, weekly, and monthly Markdown finance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive income, expense, debt, bank, or payment information may be written to plain local Markdown files.

Mitigation: Keep generated finance files in a private protected location, avoid entering raw credentials or API tokens, and delete or secure old records when no longer needed.

Risk: Broad finance-related trigger terms may activate the skill without clear consent controls.

Mitigation: Use the skill only with explicit commands and review any generated records or reports before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mesiyoq965-sudo/skills/jarvis-debt-repayment)
- [Project homepage](https://example.com/income-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, Markdown tables, inline command examples, and YAML-style configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local finance tracking files such as income-log.md, expense-log.md, debt-tracker.md, and monthly-report.md.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence, SKILL.md frontmatter, README.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
