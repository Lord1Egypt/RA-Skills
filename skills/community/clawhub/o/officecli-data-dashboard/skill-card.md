## Description:

Use this skill to build a multi-element Excel dashboard with a Dashboard sheet on open, formula-driven KPI cards, charts, sparklines, and conditional formatting from CSV or tabular input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iceyliu](https://clawhub.ai/user/iceyliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn CSV or tabular data into an Excel dashboard with KPI cards, charts, sparklines, and conditional formatting. It is intended for multi-element dashboard deliverables rather than simple formatted spreadsheets or financial models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance includes direct execution of remote installer scripts, which can be high-impact without verification.

Mitigation: Install only from a trusted OfficeCLI distribution path, prefer a pinned official release, and verify checksums or signatures before running installers.

Risk: Raw XML workbook edits can modify files in ways that are difficult to inspect manually.

Mitigation: Apply raw XML steps only to intended workbook files and validate the workbook after edits.

## Reference(s):

- [OfficeCLI releases](https://github.com/iOfficeAI/OfficeCLI/releases)
- [officecli-data-dashboard on ClawHub](https://clawhub.ai/iceyliu/skills/officecli-data-dashboard)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and spreadsheet construction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for creating a single .xlsx dashboard.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
