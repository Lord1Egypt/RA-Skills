## Description: <br>
基于 pdfplumber 本地提取增值税电子发票和火车票信息，并输出格式化 Excel，支持多税率及水印页兜底识别。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seairteng](https://clawhub.ai/user/seairteng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, operations, and administrative users can use this skill to process local invoice PDF batches and create a structured Excel summary for reimbursement or accounting workflows. It extracts invoice identifiers, dates, buyer and seller details, tax rates, amounts, totals, duplicate indicators, and train-ticket records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input PDFs and generated Excel summaries may contain sensitive financial and taxpayer information. <br>
Mitigation: Handle PDF inputs and .xlsx outputs as confidential records, store them only in approved locations, and remove them when no longer needed. <br>
Risk: Installing runtime dependencies from an untrusted package source could introduce supply-chain risk. <br>
Mitigation: Install pdfplumber and openpyxl from trusted package indexes or approved internal mirrors before running the extractor. <br>
Risk: Invoice parsing can miss or misread fields when PDFs use unusual layouts, watermarks, or OCR/text extraction edge cases. <br>
Mitigation: Review the generated Excel summary, especially blank dates, missing tax IDs, zero non-train-ticket amounts, empty item names, and highlighted duplicates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seairteng/skills/pdf-invoice-stat) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with Python shell commands and generated Excel files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local PDF invoice files and writes a formatted .xlsx summary; no network behavior is reported by the security evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
