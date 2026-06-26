## Description: <br>
支持增值税发票、普通发票、区块链发票等多种票据的OCR识别与信息提取；自动完成票据类型分类、关键字段提取、格式校验；当用户需要识别发票内容、提取发票信息、校验发票格式时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangdeqian](https://clawhub.ai/user/fangdeqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to recognize invoice images or documents, extract structured invoice fields, classify invoice types, validate field formats and totals, and receive guidance for manual official invoice verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoices may contain sensitive financial, tax, and identity information. <br>
Mitigation: Process invoice files and extracted data in a controlled environment, store outputs in approved locations, and delete temporary or converted files when no longer needed. <br>
Risk: OCR extraction, validation, and field completion can produce incorrect or inferred invoice data. <br>
Mitigation: Review extracted fields, validation failures, and any completed values before using results for accounting, tax, or verification decisions. <br>
Risk: PDF or OFD preprocessing can write converted image files to local storage. <br>
Mitigation: Use trusted input files, choose an access-controlled output directory, and remove generated images after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fangdeqian/invoice-recognition) <br>
- [发票格式规范](references/invoice-formats.md) <br>
- [票据类型分类指南](references/invoice-types.md) <br>
- [国家税务总局全国增值税发票查验平台](https://inv-veri.chinatax.gov.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON invoice extraction results and optional shell commands for document conversion] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local converted image files when processing PDF or OFD inputs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
