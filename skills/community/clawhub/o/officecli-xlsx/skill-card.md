## Description: <br>
Use this skill any time a .xlsx file is involved as input, output, or both, including creating spreadsheets, financial models, dashboards, or trackers; reading, parsing, or extracting data from .xlsx files; editing existing workbooks; working with formulas, charts, pivot tables, or templates; and importing CSV/TSV data into Excel format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iceyliu](https://clawhub.ai/user/iceyliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to read, create, edit, validate, and quality-check Excel workbooks through OfficeCLI workflows. It is aimed at spreadsheet-heavy tasks such as financial models, dashboards, trackers, workbook templates, formulas, charts, and CSV/TSV-to-XLSX conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic download and execution of an unpinned remote OfficeCLI installer or updater can introduce supply-chain risk. <br>
Mitigation: Install OfficeCLI separately from a pinned, verified release and disable or review automatic upgrade steps before using the skill. <br>
Risk: Workbook editing commands can remove, import, merge, or alter raw XML and may damage important spreadsheets if applied incorrectly. <br>
Mitigation: Work on backup copies and run OfficeCLI validation and issue checks before delivering modified workbooks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/iceyliu/officecli-xlsx) <br>
- [Creating Workbooks from Scratch](artifact/creating.md) <br>
- [Editing Existing Workbooks](artifact/editing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and OfficeCLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent instructions for workbook creation, inspection, editing, validation, and QA; generated or modified workbook files are produced by OfficeCLI commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
