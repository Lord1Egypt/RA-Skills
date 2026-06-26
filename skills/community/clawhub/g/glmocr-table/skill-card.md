## Description: <br>
Official skill for recognizing and extracting tables from images and PDFs into Markdown format using the ZhiPu GLM-OCR API, including complex tables, merged cells, and multi-page documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredforreal](https://clawhub.ai/user/jaredforreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to extract tables from images, scanned documents, PDFs, reports, invoices, and financial statements into editable Markdown or JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-selected images, PDFs, or URLs to Zhipu's GLM-OCR API using a ZHIPU_API_KEY. <br>
Mitigation: Use only documents approved for external processing; avoid confidential, regulated, or sensitive business documents unless that processing is authorized. <br>
Risk: The skill requires a sensitive Zhipu API credential. <br>
Mitigation: Store ZHIPU_API_KEY in approved environment configuration, restrict access, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [GLM-OCR Table skill homepage](https://github.com/zai-org/GLM-OCR/tree/main/skills/glmocr-table) <br>
- [Zhipu Layout Parsing API documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E6%96%87%E6%A1%A3%E8%A7%A3%E6%9E%90) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown table text and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save result JSON to a file; raw upstream responses are included only when explicitly requested for debugging.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
