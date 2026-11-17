## Description:

支持增值税发票、普通发票、区块链发票等多种票据的OCR识别与信息提取；自动完成票据类型分类、关键字段提取、格式校验；当用户需要识别发票内容、提取发票信息、校验发票格式时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangdeqian](https://clawhub.ai/user/fangdeqian)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to recognize invoices from images or documents, classify invoice types, extract structured invoice fields, and validate invoice formats and amount logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice files and extracted fields can contain sensitive personal, tax, and business information.

Mitigation: Process only user-provided invoices, prefer local or restricted processing, and avoid exposing extracted fields or converted files in shared locations.

Risk: OFD conversion requires an optional dependency that is not pinned in the artifact.

Mitigation: Pin or review the ofd2pdf package before installation and use it only in a controlled environment.

Risk: The helper script writes converted images to caller-selected output paths.

Mitigation: Use private output directories for conversions and clean up generated files after recognition is complete.

## Reference(s):

- [发票格式规范](references/invoice-formats.md)
- [票据类型分类指南](references/invoice-types.md)
- [国家税务总局全国增值税发票查验平台](https://inv-veri.chinatax.gov.cn)
- [ClawHub skill page](https://clawhub.ai/fangdeqian/skills/invoice-recognition)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with structured JSON-style invoice extraction results and optional shell commands for document conversion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted invoice fields, type classification, validation status, correction guidance, and manually performed official verification steps.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
