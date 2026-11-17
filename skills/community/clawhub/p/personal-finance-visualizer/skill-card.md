## Description:

Turn user-provided personal finance records into a local interactive report with spending, income, transfers and cash movement in English or Chinese. Use for statement-based finance charts and period comparisons, not bank-account actions or investment advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonhmy](https://clawhub.ai/user/jasonhmy)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users can turn authorized, prepared transaction records into reconciled local reports for comparing spending, income, transfers, and cash movement. It is not for bank-account actions or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports and exported HTML can contain sensitive transaction details, and a report link may expose personal financial information.

Mitigation: Share report links and exported files only with intended recipients, keep exports private, and stop the local server when finished.

Risk: Incomplete records or unresolved transaction classifications, refunds, or transfers can make report totals misleading.

Mitigation: Provide only authorized records, confirm uncertain items before final charts, and keep source coverage gaps visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jasonhmy/skills/personal-finance-visualizer)
- [Report input schema](references/schema.md)
- [Reconciliation and delivery workflow](references/workflow.md)
- [Repository declared in skill metadata](https://github.com/JasonHMY/personal-finance-visualizer)

## Skill Output:

**Output Type(s):** [HTML report, Charts, Financial summaries, Guidance]

**Output Format:** [Interactive local HTML report and concise conversational guidance in English or Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports reflect the supplied records and coverage; they are not a complete financial picture unless the user-provided data supports that scope.]

## Skill Version(s):

1.4.1 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
