## Description:

Generates quantitative strategy evaluation reports by reading Excel NAV data, calculating performance and risk metrics, creating charts, and producing PDF and Word reports with structured analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duanwei2028](https://clawhub.ai/user/duanwei2028)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn uploaded quantitative strategy Excel data into institutional-style strategy evaluation reports. It supports NAV analysis, optional instrument-level analysis, AI-authored commentary, chart generation, and PDF/DOCX report output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded Excel files and generated reports may contain sensitive financial data.

Mitigation: Run the skill in an isolated virtual environment or controlled workspace, restrict access to input and output directories, and remove generated artifacts when no longer needed.

Risk: Untrusted analysis.json files or strategy names can affect report content and generated filenames.

Mitigation: Use trusted analysis inputs and sanitize strategy names and output paths before production use.

Risk: Dependencies are documented as install commands rather than pinned in a lock file.

Mitigation: Pin dependencies or use a reviewed lock file before deploying the workflow in production.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands, JSON content requirements, PNG charts, PDF reports, and DOCX reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces analysis.json, content.json, chart PNG files, and strategy report documents in the selected output directory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
