## Description:

Historical Data Compare Claw helps agents analyze period-over-period, year-over-year, trend, and attribution differences in historical CSV or Excel data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business users use this skill to compare historical metrics across periods, identify material changes, and produce concise Chinese-language explanations or reports with supporting calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided spreadsheets may contain sensitive or confidential business data.

Mitigation: Review spreadsheet contents before sharing them with an agent and remove data that is not needed for the comparison.

Risk: Writing reports with an unspecified or unintended output location can place generated files where users do not expect them.

Mitigation: When using --output, provide a specific report path and review the destination before execution.

Risk: Incorrect date columns, metric columns, missing values, duplicates, or inconsistent comparison periods can produce misleading trend conclusions.

Mitigation: Validate data quality, column selection, and comparison periods before relying on the generated analysis.

## Reference(s):

- [Data Analysis Methodology Reference](references/methodology.md)
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/skills/historical-data-compare-claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Chinese-language Markdown reports, plain-text comparison tables, and optional report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports CSV and Excel inputs; reports may be printed to stdout or written to a user-specified output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
