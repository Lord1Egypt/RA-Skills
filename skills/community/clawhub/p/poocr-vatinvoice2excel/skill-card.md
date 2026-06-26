## Description: <br>
使用 poocr 库识别发票并导出 Excel。当用户需要识别增值税发票、批量处理发票文件或提取发票信息到 Excel 时调用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CoderWanFeng](https://clawhub.ai/user/CoderWanFeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, tax, audit, and data-entry users can use this skill to recognize VAT invoices from PDF, JPG, or PNG files and export extracted invoice fields to Excel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice files and exported Excel results may contain sensitive financial or personal data. <br>
Mitigation: Confirm the files may be processed with Tencent Cloud and protect both source invoices and generated Excel files according to the user's data-handling requirements. <br>
Risk: Tencent Cloud API credentials can be exposed if copied into shared code or logs. <br>
Mitigation: Use a limited Tencent Cloud API key and avoid hardcoding real secrets in reusable examples or shared repositories. <br>
Risk: Batch processing can include unintended files when pointed at a broad folder. <br>
Mitigation: Process only the intended folder and review generated Excel output before relying on it. <br>


## Reference(s): <br>
- [Tencent Cloud API key console](https://curl.qcloud.com/9ExTmaya) <br>
- [ClawHub skill page](https://clawhub.ai/CoderWanFeng/poocr-vatinvoice2excel) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for generating Excel files from invoice OCR results; users provide local invoice paths, an output directory, and Tencent Cloud credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
