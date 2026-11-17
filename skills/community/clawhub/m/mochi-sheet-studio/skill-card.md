## Description:

Combine XLSX/CSV sources, clean mapped fields, deduplicate, reconcile sales, refunds, and expenses, and export currency-separated monthly reports with source rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Business analysts and operations staff use the skill to prepare repeatable local sales, refund, and expense summaries or reconcile two spreadsheets, with issue rows and source locations for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports retain transaction details.

Mitigation: Keep generated reports private and limit access to intended reviewers.

Risk: Excluded or invalid rows can affect reported totals.

Mitigation: Choose an explicit YYYY-MM reporting period and review the report's Issues before relying on totals.

Risk: Different local environments or dependency versions can affect reproducibility.

Mitigation: Use a dedicated virtual environment and reviewed installer and dependency versions.

## Reference(s):

- [Job contract](references/input.md)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-sheet-studio)
- [MochiLab homepage](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Files, Analysis, Configuration]

**Output Format:** [Excel workbook, JSON reports and recipe, and HTML preview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports keep source row locations, separate currencies, and retain exact decimal strings in JSON.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
