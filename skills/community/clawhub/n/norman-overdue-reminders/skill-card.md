## Description: <br>
Finds overdue invoices, groups them by reminder severity, and helps send payment reminders only after user review and approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanlee000](https://clawhub.ai/user/stanlee000) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Finance operators and business users use this skill to review unpaid Norman Finance invoices, decide which clients should receive reminders, and approve each reminder before it is sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access invoice, client, and transaction data through the Norman Finance MCP. <br>
Mitigation: Install it only for users who should view this financial data and review invoice, client, and amount details before taking action. <br>
Risk: Payment reminders and formal Mahnung workflows can affect customer relationships or create legal implications, especially outside Germany. <br>
Mitigation: Review the recipient, due date, amount, reminder tone, and local legal context before approving any send. <br>
Risk: A reminder could be sent for an invoice that was recently paid but not yet linked. <br>
Mitigation: Check recent transactions before approving reminders when payment status is uncertain. <br>


## Reference(s): <br>
- [Norman Finance](https://norman.finance) <br>
- [ClawHub skill page](https://clawhub.ai/stanlee000/norman-overdue-reminders) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown tables, reminder drafts, approval prompts, and final summary reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Norman Finance MCP; reminder sends require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
