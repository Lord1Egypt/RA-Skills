## Description:

Checks Chinese overtime-pay worksheets with deterministic arithmetic recalculation, total reconciliation, duplicate detection, blank-field detection, and source line references for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

HR and finance staff use this skill before payroll runs to check overtime-pay worksheets for arithmetic mismatches, missing fields, duplicate personnel rows, and total-row inconsistencies. It supports review of the worksheet math only and does not determine whether overtime records are legally valid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payroll worksheet inputs may contain employee names and compensation data.

Mitigation: Run the checker locally and provide only the rows and fields needed for the overtime arithmetic check.

Risk: The result can be mistaken for legal validation of overtime records.

Mitigation: Use the output only as an arithmetic worksheet check; have qualified personnel review approval status, attendance truthfulness, and labor-law questions separately.

Risk: The free edition omits some checks such as monthly overtime-hour limits, minimum-wage comparisons, invalid negative values, and unusual pay-day counts.

Mitigation: Review the listed omitted checks and add separate controls when those issues matter for the payroll review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/overtime-pay-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable console output or JSON report with findings, source line references, summary totals, omitted checks, and assumptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; output should be treated as an arithmetic check, not legal advice.]

## Skill Version(s):

1.0.35 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
