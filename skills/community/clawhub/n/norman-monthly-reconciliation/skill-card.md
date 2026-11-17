## Description:

Perform a complete monthly financial reconciliation - review all transactions, match invoices, check outstanding payments, and prepare for tax filing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanlee000](https://clawhub.ai/user/stanlee000)

### License/Terms of Use:


## Use Case:

Employees and finance operators use this skill to close a monthly accounting period by reviewing transactions, reconciling invoices and payments, checking receipts, preparing tax overviews, and summarizing outstanding actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify accounting records and initiate finance workflows through the Norman Finance MCP.

Mitigation: Confirm the target month and review each proposed categorization, verification, reminder, and tax action before allowing the skill to proceed.

Risk: Month-end reconciliation may produce incorrect bookkeeping outcomes if missing receipts, unclear categories, or unpaid invoices are accepted without review.

Mitigation: Require user review for flagged missing information and outstanding items before marking the period complete.

## Reference(s):

- [Norman Finance](https://norman.finance)
- [ClawHub skill page](https://clawhub.ai/stanlee000/skills/norman-monthly-reconciliation)

## Skill Output:

**Output Type(s):** [guidance, text, API Calls]

**Output Format:** [Markdown guidance with proposed finance actions and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before sensitive final actions such as tax submission.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
