## Description:

Personal expense tracker that records expenses, auto-categorizes entries, and reports monthly totals with category breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to record personal expenses, categorize spending notes, list recent entries, and summarize monthly spending totals and category shares.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Expense records and generated spending summaries may be stored locally in plaintext.

Mitigation: Use only with financial data acceptable for local plaintext storage, restrict permissions on the data directory, and review storage behavior before deployment.

Risk: The stats behavior can create an extra local summary file without clearly disclosing that side effect to users.

Mitigation: Change the stats workflow to ask before saving or exporting summaries, or remove the extra summary write before using the skill with real financial data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/personal-expense-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and plaintext expense summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store expense records and generated spending summaries locally in plaintext when commands are executed.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and _meta.json report v1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
