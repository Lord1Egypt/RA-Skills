## Description: <br>
Automatically merge reimbursement folders into one PDF, including recursive folder scanning, PDF merging, two invoices per A4 page, phone screenshots and images as A4 half-page slots, and Excel workbooks with multiple sheets converted to PDF before merging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harven-droid](https://clawhub.ai/user/harven-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents preparing reimbursement packets use this skill to merge local PDFs, images, and Excel workbooks into a checked reimbursement PDF. It is intended for reimbursement submission or print/archive workflows where the generated PDF, report, and thumbnails can be reviewed before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install Python packages and LibreOffice through pip or system package managers unless disabled. <br>
Mitigation: Use a trusted environment, install pinned dependencies manually, or run with --no-auto-install or MERGE_TRAVEL_PDFS_NO_AUTO_INSTALL=1. <br>
Risk: Broad folder inputs can include unintended reimbursement materials or generated outputs. <br>
Mitigation: Point the skill at a dedicated reimbursement folder, review the JSON report and render-check thumbnails, and confirm warnings before delivering the merged PDF. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harven-droid/merge-reimbursement-pdfs) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [PDF output files with JSON reports and optional PNG render-check thumbnails; Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local PDF, image, and Excel files; supports dry-run classification, split-subfolder output, rendered checks, and manual invoice classification overrides.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
