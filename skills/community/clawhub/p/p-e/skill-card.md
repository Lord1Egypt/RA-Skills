## Description: <br>
P-E extracts structured data from a template image and matching data images, then generates an Excel workbook with embedded images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haiou-max](https://clawhub.ai/user/haiou-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn product or tabular image batches into a structured Excel workbook. It is intended for workflows where a template image defines fields and subsequent images provide repeated records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install Python packages during dependency checks. <br>
Mitigation: Review the setup path before use and run dependency installation in a controlled Python environment. <br>
Risk: The skill can create an Excel file and retain local image copies under `/tmp/p-e-images/`. <br>
Mitigation: Use only images approved for local storage, choose an appropriate output path, and delete temporary image copies after completion. <br>
Risk: The skill can write local files automatically without a confirmation step. <br>
Mitigation: Review requested inputs and output paths before invoking it in a workspace with sensitive files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haiou-max/p-e) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files] <br>
**Output Format:** [Markdown status report, JSON intermediate data, shell commands, and Excel workbook file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates an .xlsx workbook with formatted columns and embedded images; may write temporary JSON and image files during execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
