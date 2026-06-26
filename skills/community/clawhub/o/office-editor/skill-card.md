## Description: <br>
Helps an agent create or modify Word (.docx), Excel (.xlsx), and PowerPoint (.pptx) files while checking required Python document libraries before making changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Noah-Wu66](https://clawhub.ai/user/Noah-Wu66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and knowledge workers use this skill to generate or update Office documents from agent workflows. It is useful for document export, spreadsheet creation, presentation drafting, and structured edits to existing local Office files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scripts or edits can overwrite or alter local Office documents if pointed at the wrong filename. <br>
Mitigation: Review target filenames before running generated scripts, preserve originals by default, and overwrite only when explicitly intended. <br>
Risk: Office document creation depends on local Python libraries such as python-docx, openpyxl, and python-pptx. <br>
Mitigation: Check imports before implementation and report missing packages directly instead of installing dependencies automatically. <br>


## Reference(s): <br>
- [Office-Editor on ClawHub](https://clawhub.ai/Noah-Wu66/office-editor) <br>
- [python-docx API Summary](references/docx_api_summary.md) <br>
- [python-pptx API Quick Reference](references/pptx_api_reference.md) <br>
- [PowerPoint Chart Creation Guide](references/pptx_chart_guide.md) <br>
- [Excel Charts Reference](references/xlsx_charts.md) <br>
- [Excel Advanced Features Reference](references/xlsx_features.md) <br>
- [Excel pandas Integration Reference](references/xlsx_pandas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets and generated or modified Office files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local .docx, .xlsx, and .pptx files when the required Python libraries are available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
