## Description:

基金月报信息提取，支持单文件上传和批量处理文件夹，可自动学习Excel模板并从PDF月报提取数据生成PDF信息Excel和用户模板Excel。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujing2013](https://clawhub.ai/user/yujing2013)

### License/Terms of Use:

MIT-0

## Use Case:

External fund operations and analysis users can use this skill to extract monthly fund data from user-provided PDFs and populate Excel workbooks. It is intended for local document processing where generated financial data is reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad or automatic file processing could include more PDFs, Excel files, ZIP contents, or folders than intended.

Mitigation: Provide only specific input paths, avoid broad folders, and confirm the selected files before running batch processing.

Risk: Generated financial data may be incomplete or inaccurate because PDF text extraction and OCR can miss or misread values.

Mitigation: Treat generated workbooks as drafts and manually verify extracted figures against the source monthly reports before business use.

Risk: Installing Python and OCR/PDF dependencies can introduce package or local toolchain risk.

Mitigation: Install dependencies in an isolated environment using trusted, pinned packages and verified OCR/PDF tools.

Risk: The skill instructions may describe broader automation than the scripts reliably provide.

Mitigation: Review the selected workflow before execution and do not rely on automatic timeout processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yujing2013/skills/mutual-fund-monthly-update)
- [Publisher profile](https://clawhub.ai/user/yujing2013)
- [Security review](SECURITY_REVIEW.md)
- [Batch processing guide](references/batch_processing.md)
- [Field mapping rules](references/field_mapping.md)
- [Interaction rules](references/interaction_rules.md)
- [OCR rules](references/ocr_rules.md)
- [Template learning guide](references/template_learning.md)
- [Extraction templates](references/extraction_templates.json)

## Skill Output:

**Output Type(s):** [files, code, shell commands, guidance]

**Output Format:** [Excel workbooks plus concise status text and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes user-selected PDFs, Excel templates, ZIP files, or folders locally and produces workbook outputs that should be manually reviewed.]

## Skill Version(s):

2.3.0 (source: server release evidence; artifact frontmatter reports 2.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
