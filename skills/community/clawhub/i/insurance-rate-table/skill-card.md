## Description:

Generates standardized Excel two-dimensional insurance rate tables from user-provided product parameters, including plans, payment periods, payment methods, receive ages, ages, and gender groupings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyanhe95](https://clawhub.ai/user/liyanhe95)

### License/Terms of Use:

MIT-0

## Use Case:

Insurance product teams, developers, and analysts use this skill to collect product parameters and generate a structured .xlsx rate table with multi-level headers and filtered payment combinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated output paths may be unsafe when product names contain path-like text.

Mitigation: Use the skill only in a contained workspace and reject product names containing slashes, backslashes, dot-dot traversal, or similar path-like content.

Risk: The spreadsheet dependency identified in the security evidence may be vulnerable.

Mitigation: Update or replace the xlsx dependency before handling untrusted spreadsheet-related inputs.

## Reference(s):

- [Insurance rate table format standard](references/format-standard.md)
- [ClawHub skill page](https://clawhub.ai/liyanhe95/skills/insurance-rate-table)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Excel .xlsx file with concise Markdown status and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a workbook named from the product name, with a sheet named 费率表 and a five-row multi-level header.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
