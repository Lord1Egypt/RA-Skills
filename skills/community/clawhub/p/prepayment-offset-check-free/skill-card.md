## Description:

A local Chinese-language prepayment ledger checker that recomputes row arithmetic, total cross-checks, duplicates, and blank required fields, with source-cited findings for the free check set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

Proprietary

## Use Case:

Finance and accounting users use this skill during monthly close, reconciliation, or inventory review to check prepayment offset ledgers for arithmetic mismatches, total-row inconsistencies, duplicate supplier-contract rows, and blank required fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs bundled Node.js code on user-supplied prepayment ledger text.

Mitigation: Install and run it only if local execution of this checker is acceptable in the target environment.

Risk: The free version intentionally omits several checks reserved for the full version.

Mitigation: Review the reported checks_not_run before relying on the result as a complete prepayment-ledger review.

Risk: The interface and results are Chinese-only.

Mitigation: Use reviewers who can read the Chinese output or translate the findings before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/prepayment-offset-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable console output or JSON containing executed checks, findings, summary, omitted checks, and scope metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with bundled Node.js code; the interface and result text are Chinese-only.]

## Skill Version(s):

1.0.55 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
