## Description:

Extract, clean, and organize legacy construction data from archives. Migrate historical project data, cost records, and schedules into modern formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction data teams, estimators, and developers use this skill to extract, clean, normalize, and migrate legacy project, cost, schedule, labor, and material records for benchmarking, productivity analysis, risk review, and estimating calibration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed dependencies or legacy database drivers may introduce supply-chain or runtime risk.

Mitigation: Install dependencies in an isolated environment with pinned and reviewed versions.

Risk: Archive scanning may read unintended project folders if pointed at a broad filesystem path.

Mitigation: Point the skill only at intended archive folders and validate input paths before processing.

Risk: Formula-like text in legacy records can create spreadsheet injection risk when exported to Excel or opened in generated workbooks.

Mitigation: Sanitize formula-like text before exporting legacy data to Excel or opening generated workbooks.

## Reference(s):

- [Datadriven Construction homepage](https://datadrivenconstruction.io)
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/historical-data-manager)
- [Publisher profile](https://clawhub.ai/user/datadrivenconstruction)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured tables, Python code snippets, shell commands, and optional CSV, Excel, or JSON export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize data quality, normalized costs, detected file types, and migration findings from user-provided archive data.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
