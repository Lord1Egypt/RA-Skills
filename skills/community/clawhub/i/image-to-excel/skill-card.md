## Description: <br>
Extract table content from images, retrieve row/column data, correct recognition errors, and generate a well-formatted Excel file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to convert images containing tables into corrected row and column data and a formatted Excel workbook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install openpyxl at runtime if the dependency is missing. <br>
Mitigation: Review before installing, and prefer preinstalling or pinning openpyxl in a controlled environment. <br>
Risk: The Excel writer saves to the requested output path and may overwrite an existing file. <br>
Mitigation: Use a non-existing or disposable output filename when generating workbooks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/image-to-excel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON table data, an .xlsx file, and a short preview of extracted rows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Excel writer pads inconsistent rows, styles the first row as a header when multiple rows exist, freezes the header row, and auto-sizes columns.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
