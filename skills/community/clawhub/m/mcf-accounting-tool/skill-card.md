## Description: <br>
Financial management with invoices, expenses, job costing, P&L reports, and QuickBooks sync for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cameron48](https://clawhub.ai/user/cameron48) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage accounting workflows such as invoice creation and sending, expense logging, job-cost tracking, P&L reporting, and QuickBooks synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable agents to create financial records, send invoices, mark invoices paid, and sync accounting data without clear approval limits. <br>
Mitigation: Require human approval for mutating accounting actions and use sandbox or least-privilege accounting accounts until authorization scopes and audit controls are clear. <br>
Risk: QuickBooks synchronization can propagate incorrect or unauthorized accounting changes into a traditional accounting system. <br>
Mitigation: Approve sync operations explicitly, review sync logs, and limit connected QuickBooks permissions to the minimum needed. <br>
Risk: Each endpoint call requires x402 USDC payment on Base L2, so automated use can incur costs. <br>
Mitigation: Set spending limits and require confirmation for higher-cost or repeated paid calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cameron48/mcf-accounting-tool) <br>
- [MCF Agentic gateway](https://gateway.mcfagentic.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Configuration] <br>
**Output Format:** [Markdown with accounting API endpoints, payment notes, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires x402 USDC payment on Base L2 for each call.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
