## Description:

A free deterministic checker for piece-rate wage sheets that recomputes piece wages and net payable amounts row by row, cross-foots total lines, and flags duplicates, blanks, negative values, and qualified-quantity mismatches with source line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing, apparel, and electronics assembly payroll teams use this skill before wage runs to check pasted piece-rate wage tables for arithmetic and cross-footing errors. It supports local review of table-internal calculations, not payroll compliance approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free release does not validate standard process rates, recompute whether minimum-wage top-up is correct, detect duplicate rework or scrap deductions, or provide legal/payroll compliance advice.

Mitigation: Review the output's checks_not_run list before relying on results, and use separate payroll, legal, or full-control review for omitted checks.

Risk: Missing or unrecognized wage-table columns can prevent checks from running or limit the conclusions.

Mitigation: Confirm scope.missing_columns, scope.skipped_checks, and checks_not_run after each run, and provide wage-table text with complete headers.

Risk: A clean arithmetic result may be mistaken for full payroll approval.

Mitigation: Treat the output as a table-internal arithmetic checker only, and require human payroll review before wage disbursement.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/chenqg618/skills/piece-rate-wage-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable console text or structured JSON with scope, findings, summary, omitted checks, and source line references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on wage-table text; insufficient input returns missing requirements instead of a payroll verdict.]

## Skill Version(s):

1.0.49 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
