## Description: <br>
基金月报信息提取。支持单文件上传和批量处理文件夹。自动学习Excel模板，从PDF月报提取数据，生成两份Excel（PDF信息Excel + 用户模板Excel）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yujing2013](https://clawhub.ai/user/Yujing2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to extract data from mutual fund monthly report PDFs, optionally learn an Excel template, and generate updated Excel workbooks for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive financial PDFs and Excel templates from user-selected paths. <br>
Mitigation: Use a dedicated folder containing only intended files and confirm selected paths before processing. <br>
Risk: The skill writes generated spreadsheets that may contain OCR or field-mapping errors. <br>
Mitigation: Review generated financial data manually before relying on or sharing the Excel output. <br>
Risk: Spreadsheet output paths may be incorrect or broader than intended. <br>
Mitigation: Verify output paths before writing files and require explicit final confirmation before processing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Yujing2013/mutual-fund-monthly-update) <br>
- [Batch Processing](references/batch_processing.md) <br>
- [Field Mapping](references/field_mapping.md) <br>
- [Interaction Rules](references/interaction_rules.md) <br>
- [OCR Rules](references/ocr_rules.md) <br>
- [Template Learning](references/template_learning.md) <br>
- [Extraction Templates](references/extraction_templates.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for local PDF and Excel processing; generated financial data should be manually reviewed.] <br>

## Skill Version(s): <br>
2.3.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
