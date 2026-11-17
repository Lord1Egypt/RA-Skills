## Description:

A deterministic local checker for land appreciation tax prepayment and settlement worksheets that recomputes deductions, appreciation amount and rate, tax payable, prepayment tax due, total rows, duplicates, blanks, and prepayment differences with source line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Project accountants at real estate and construction companies use this skill to check land appreciation tax prepayment and settlement worksheets before filing or reconciliation. It helps identify arithmetic inconsistencies, missing key fields, duplicate projects, negative values in non-negative columns, and total-row mismatches.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may treat worksheet arithmetic findings as tax advice or as validation of a tax position.

Mitigation: Use the output as a consistency check only, and verify tax positions against source documents or a qualified professional.

Risk: The checker does not validate local policy rates, prepayment rates, or whether expenses are eligible for deduction.

Mitigation: Confirm that worksheet rates and deductible items are appropriate before relying on any recalculated amounts.

Risk: Incomplete inputs, missing headers, or unsupported spreadsheet files may produce insufficient-input results rather than findings.

Mitigation: Provide a complete table with headers as text or JSON, and export spreadsheet data before running the checker.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/land-appreciation-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)
- [Skill usage documentation](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON findings with worksheet line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; insufficient input returns missing-field guidance rather than a pass/fail conclusion.]

## Skill Version(s):

1.0.21 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
