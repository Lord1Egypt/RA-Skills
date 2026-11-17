## Description:

Generate professional PDF invoices from simple text commands with multiple currencies, tax calculation, CJK text support, and no external service requirement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zacjiang](https://clawhub.ai/user/zacjiang)

### License/Terms of Use:


## Use Case:

External users, freelancers, and small-business operators use this skill to create print-ready PDF invoices from natural language or structured billing details. Agents can call the bundled script to calculate subtotals, tax, totals, invoice numbers, due terms, notes, and currency-formatted line items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance includes optional sudo package-install commands for CJK fonts that modify system packages.

Mitigation: Run those commands only in an appropriate environment and only after reviewing the package source and system impact.

Risk: The PDF generator depends on ReportLab.

Mitigation: Install the dependency in a virtual environment and pin ReportLab to a reviewed version before operational use.

Risk: The release advertises customizable templates, while the security guidance says to verify or extend that capability before relying on it.

Mitigation: Review the bundled script and add the required template controls before promising customized invoice layouts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zacjiang/skills/invoice-gen)
- [Publisher profile](https://clawhub.ai/user/zacjiang)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PDF file plus Markdown guidance with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local invoice PDFs using ReportLab; supports itemized billing, tax calculation, multiple currencies, optional notes, and optional CJK font support.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
