## Description:

Generate standardized HR workforce dashboards from Excel files: 5 fixed dashboards covering headcount trends, regional distribution, detailed breakdowns, attrition analysis, and contractor/partner distribution. Outputs a self-contained interactive HTML with ECharts charts, one-click email generation, and clipboard copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aico233](https://clawhub.ai/user/aico233)

### License/Terms of Use:

MIT-0

## Use Case:

HR and people-analytics users use this skill to turn active employee, termination, and contingent worker Excel extracts into standardized workforce dashboards for headcount, attrition, and regional distribution reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated dashboards may contain sensitive HR material.

Mitigation: Use a dedicated workspace output folder, restrict access to generated files, and verify recipients before using email or clipboard features.

Risk: Using an existing output directory can delete or overwrite files.

Mitigation: Create a new empty output directory for each run and do not point --output-dir at an existing project or personal directory.

Risk: dashboard.html loads ECharts from jsDelivr.

Mitigation: Open the dashboard only in environments where remote JavaScript from jsDelivr is permitted, or review the asset policy before sharing.

## Reference(s):

- [Workforce Data Spec](references/data_spec.md)
- [Field Mapping](references/field_mapping.md)
- [Metric Definitions](references/metric_definitions.md)
- [Layout Spec](references/layout_spec.md)
- [Install and Examples](references/install_and_examples.md)
- [ClawHub Skill Page](https://clawhub.ai/aico233/skills/hr-workforce-dashboard)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [Self-contained HTML dashboard plus optional ZIP bundle, PNG images, Excel workbook, PowerPoint deck, and Markdown summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary output is dashboard.html; Dashboard 5 requires contingent worker input; degraded sections are marked when source files are missing.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
