## Description: <br>
AR/AP invoice automation for PrecisionLedger that supports aging analysis, overdue follow-up drafting, payment matching, and collection priority scoring while keeping accounting-system changes and client communications behind human approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting and finance teams use this skill to analyze AR/AP aging, draft overdue invoice follow-ups, match incoming payments to open invoices, and prioritize collections. It is designed for recommendation and drafting workflows, with human review before communications or accounting-system changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice, client, and payment data can be sensitive. <br>
Mitigation: Provide only the data needed for the task and use the skill only where the agent is permitted to process AR/AP workflow data. <br>
Risk: Drafted collections messages, payment matches, or priority scores may be incorrect or inappropriate for a specific account. <br>
Mitigation: Review amounts, invoice IDs, payment status, tone, and next actions before sending messages or making accounting decisions. <br>
Risk: The artifact explicitly disallows posting transactions, write-offs, dispute resolution, and unapproved client communications. <br>
Mitigation: Use outputs as recommendations and briefings; keep accounting-system updates, dispute handling, and outbound communications under human control. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samledger67-dotcom/invoice-automation) <br>
- [Publisher Profile](https://clawhub.ai/user/samledger67-dotcom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown tables, drafted email text, CSV exports on request, and concise recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Follow-up drafts require human approval before sending; payment matches and collection priorities should be reviewed before action.] <br>

## Skill Version(s): <br>
98.0.1 (source: ClawHub release metadata; artifact frontmatter version: 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
