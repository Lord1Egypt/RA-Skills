## Description: <br>
Generate clean A4 PDF reports from structured JSON using Jinja2 and WeasyPrint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xvespertine](https://clawhub.ai/user/0xvespertine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to convert workspace JSON report data, tables, and chart references into clean A4 PDFs for analytical summaries, data reports, and exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs system packages and Python dependencies and creates a persistent local virtual environment. <br>
Mitigation: Install only after reviewing the apt-get and pip commands, prefer a pinned or freshly recreated virtual environment, and remove ~/.openclaw/workspace/.venv_pdf when the skill is no longer used. <br>
Risk: Report inputs, outputs, templates, and chart paths touch local workspace files. <br>
Mitigation: Keep input and output paths inside the workspace and review warnings for missing or skipped chart images before relying on the PDF. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xvespertine/pdf-report) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, JSON status] <br>
**Output Format:** [PDF file with optional HTML debug output and JSON status on stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, WeasyPrint, Jinja2, and WeasyPrint system libraries; input, output, template, and chart paths are constrained to the workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
