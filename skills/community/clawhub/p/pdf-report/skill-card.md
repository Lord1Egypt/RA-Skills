## Description:

Generates clean A4 PDF reports from structured JSON using Jinja2 and WeasyPrint for analytical summaries, data reports, and chart-based exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xvespertine](https://clawhub.ai/user/0xvespertine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent operators use this skill to turn workspace JSON data into formatted A4 PDF reports with summaries, sections, tables, charts, footers, and optional debug HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom Jinja2 templates can affect rendered HTML and PDF output more broadly than ordinary report data.

Mitigation: Use only trusted custom templates and review template content before rendering.

Risk: PDF generation and template rendering may run in an environment with access to local files or sensitive environment variables.

Mitigation: Run the skill in a low-privilege or isolated workspace and avoid exposing sensitive environment variables during rendering.

Risk: Unpinned Python dependencies or system package installation can change host behavior over time.

Mitigation: Pin Python dependencies before production use and approve the sudo system package install only after reviewing the host changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PDF file, optional HTML file, and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus WeasyPrint and Jinja2 dependencies; all input, output, template, and chart paths are constrained to the workspace.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
