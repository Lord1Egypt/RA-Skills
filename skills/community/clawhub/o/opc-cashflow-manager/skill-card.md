## Description:

Cash flow decision system for solo founders that supports probability-weighted forecasting, runway calculation, burn rate analysis, survival alerts, and optional invoice-manager integration while avoiding full accounting advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonfjr](https://clawhub.ai/user/leonfjr)

### License/Terms of Use:

MIT-0

## Use Case:

Solo founders and one-person companies use this skill to maintain local cash-flow snapshots, produce conservative forecasts, evaluate runway and burn rate, prioritize collections, and identify cost cuts. It is intended for cash-flow visibility and escalates accounting, tax, investment, payroll, and similar professional-advice questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and stores sensitive local business cash-flow snapshots and optional invoice records.

Mitigation: Confirm the cashflow and invoice directories before use, restrict access to generated snapshots, and treat reports as sensitive financial records.

Risk: Forecasts and cost-cutting guidance can be misleading if inputs are stale, optimistic, or incomplete.

Mitigation: Verify source amounts and dates, review the conservative scenario first, and refresh snapshots before making cash decisions.

Risk: The skill is not a substitute for accounting, tax, investment, payroll, or legal advice.

Mitigation: Use it for cash-flow visibility and escalate professional-advice questions to the appropriate advisor.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leonfjr/skills/opc-cashflow-manager)
- [Cash Flow Forecasting Rules](references/forecasting-rules.md)
- [Runway Calculation and Survival Math](references/runway-guide.md)
- [Cost-Cutting Playbook for Solo Founders](references/cost-cutting-playbook.md)
- [Cash Flow Snapshot Schema](templates/cashflow-metadata-schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON cash-flow snapshots, and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local cashflow snapshots and can optionally import invoice records from invoices/INDEX.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
