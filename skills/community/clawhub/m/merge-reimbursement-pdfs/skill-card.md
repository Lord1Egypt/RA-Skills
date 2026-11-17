## Description:

Automatically merge reimbursement folders into one PDF, with recursive folder scanning, PDF merging, two invoices per A4 page, phone screenshots and images placed as A4 half-page slots, and Excel workbooks converted to PDF before merging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harven-droid](https://clawhub.ai/user/harven-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to prepare reimbursement packets by merging PDFs, images, invoices, travel verification sheets, and Excel workbooks into checked PDF outputs with reports and preview images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install Python packages and LibreOffice on the host by default.

Mitigation: Review before installation, use a controlled environment or virtual environment, preinstall dependencies where possible, and run with --no-auto-install or MERGE_TRAVEL_PDFS_NO_AUTO_INSTALL=1.

Risk: The render-check option may remove matching page-*.png files in its target directory.

Mitigation: Point --render-check at a dedicated empty directory for generated preview images.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated local PDF, JSON report, and PNG preview files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local files from user-provided reimbursement folders; Excel conversion requires LibreOffice or soffice.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
