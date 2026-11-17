## Description:

Extracts product label data from text-based PDF files, including product codes, names, batches, and quantities, and exports the structured result to Excel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangshouxin](https://clawhub.ai/user/zhangshouxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users use this skill to extract structured product label information from text PDFs and save it as an Excel spreadsheet for review, validation, or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing dependencies directly into a system Python environment can affect other projects or require elevated privileges.

Mitigation: Install and run the skill in a dedicated virtual environment, and avoid running pip as an administrator.

Risk: Unpinned dependencies can change behavior across installs.

Mitigation: Pin dependency versions before repeatable or production use.

Risk: The configured Excel output path could overwrite an important spreadsheet.

Mitigation: Choose and review the output filename before execution.

Risk: The package references script and reference-image files that are not included in the artifact evidence.

Mitigation: Confirm required files are present before relying on the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangshouxin/skills/my-pdf-extract-skill)
- [pdfplumber documentation](https://github.com/jsvine/pdfplumber)
- [pandas documentation](https://pandas.pydata.org/)
- [OpenClaw skills documentation](https://docs.openclaw.ai/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation of an Excel output file from a configured text PDF input.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
