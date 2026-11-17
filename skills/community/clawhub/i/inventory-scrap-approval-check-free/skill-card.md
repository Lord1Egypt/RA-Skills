## Description:

Checks inventory scrap and approval ledgers for row-level arithmetic, totals, duplicate batches, blanks, and negative values, with each finding tied to source text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations staff use this skill during monthly close, reconciliation, or inventory counts to check inventory scrap and approval ledgers before moving to downstream review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker reads local inventory scrap and approval ledger text, which may contain sensitive business records.

Mitigation: Run it only in an environment approved for the ledger data and provide only the files needed for the check.

Risk: The free version omits several approval, negative-inventory, unit-cost, and scrap-rate checks.

Mitigation: Review the reported checks_not_run and out-of-scope items before treating the result as complete.

Risk: The tool checks ledger arithmetic and internal consistency, not tax deductibility or accounting policy compliance.

Mitigation: Use the output as reconciliation evidence and confirm tax, approval, and accounting treatment with the relevant business owners.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/inventory-scrap-approval-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite input lines; insufficient input returns missing requirements instead of a conclusion.]

## Skill Version(s):

1.0.57 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
