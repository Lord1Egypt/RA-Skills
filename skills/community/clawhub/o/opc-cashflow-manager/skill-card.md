## Description: <br>
Cash flow decision system for solo founders that provides probability-weighted forecasting, runway calculation, burn rate analysis, survival alerts, and optional invoice integration without acting as full accounting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeonFJR](https://clawhub.ai/user/LeonFJR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Solo founders and one-person companies use this agent to maintain cash-flow snapshots, forecast inflows and outflows, calculate runway, prioritize collections and cost cuts, and surface survival alerts. It is intended for cash-flow visibility and decision support, not accounting, tax, payroll, investment, or bookkeeping advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cashflow snapshots, reports, and imported invoice data can contain sensitive business finance records. <br>
Mitigation: Install only from a trusted source, run the skill only against intended cashflow and invoice folders, and treat generated files as private business records. <br>
Risk: Cash-flow recommendations may be mistaken for accounting, tax, payroll, investment, or bookkeeping advice. <br>
Mitigation: Use the skill for cash visibility only and escalate accounting, tax, financing, payroll, depreciation, and accrual questions to qualified professionals. <br>
Risk: Cost-cut or cancellation suggestions can disrupt contracts, data access, operations, or rollback paths. <br>
Mitigation: Before cancelling subscriptions or services, check contracts, data export needs, operational dependencies, and recovery options. <br>


## Reference(s): <br>
- [Cash Flow Forecasting Rules](references/forecasting-rules.md) <br>
- [Runway Guide](references/runway-guide.md) <br>
- [Cost-Cutting Playbook](references/cost-cutting-playbook.md) <br>
- [Cashflow Metadata Schema](templates/cashflow-metadata-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON cash-flow snapshots, and optional CLI JSON or human-readable output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses decimal-safe amount strings, three forecast scenarios, and local cashflow snapshot/index files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
