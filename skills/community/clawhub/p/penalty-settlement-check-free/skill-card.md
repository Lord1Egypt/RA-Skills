## Description:

A free deterministic checker for penalty and liquidated-damages ledgers that recomputes balances, reconciles totals, detects duplicate document numbers, missing fields, direction or sign mismatches, and date-order issues with source line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

Proprietary

## Use Case:

Finance, accounting, and treasury users use this skill to check penalty and liquidated-damages ledgers before monthly close or annual tax settlement. It focuses on table-internal arithmetic and consistency checks, not tax or legal determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ledger inputs may contain sensitive accounting or counterparty information.

Mitigation: Use only files the user is authorized to process; evidence reports local execution without network use or persistence.

Risk: Findings cover deterministic ledger consistency checks and are not tax or legal advice.

Mitigation: Have qualified finance, tax, or legal reviewers evaluate decisions that depend on deductibility, liability, penalties, or regulatory interpretation.

Risk: The free version withholds several checks, including tax-adjustment, overdue receivable, missing-basis, cross-period, same-matter duplicate, and prioritized action-list checks.

Mitigation: Review the reported checks_run and checks_not_run fields before relying on the result, and use the output only for the disclosed free checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/penalty-settlement-check-free)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON result objects with line-referenced findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-supplied ledger text and reports checks run, checks withheld, summary totals, findings, and insufficient-input guidance.]

## Skill Version(s):

1.0.53 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
