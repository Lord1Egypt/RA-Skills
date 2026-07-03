## Description: <br>
Drive a month-end accounting close on Odoo through odoo-mcp: AR/AP aging, open-item and draft-invoice review, reconciliation checklists, and chatter documentation, with human sign-off at every posting step. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuanle96](https://clawhub.ai/user/tuanle96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance operators and business application agents use this skill to run an Odoo month-end close review, compare baseline and final accounting health, inspect aging and draft invoices, and document approved close actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews sensitive Odoo accounting data. <br>
Mitigation: Install only when the agent is intended to review finance records, and limit odoo-mcp permissions to the relevant company and accounting records. <br>
Risk: Posting, deletion, reconciliation, field changes, or chatter documentation could change business records. <br>
Mitigation: Verify every previewed write and require explicit human approval before executing any write action. <br>
Risk: Multi-company Odoo access can hide records outside the active company scope. <br>
Mitigation: Confirm company scope before close review work and use access diagnostics when visibility is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuanle96/skills/odoo-month-end-close) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown close report with summary tables, action records, approval-token events, and carried-over items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tool-derived accounting figures and explicit human approval before posting, deletion, reconciliation, field changes, or chatter documentation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
