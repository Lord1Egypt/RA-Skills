## Description: <br>
进出口许可文档智能预审系统，可处理 PDF 和图片，自动提取合同号、出口国、进口商、总金额、数量、重量、合格证编号、生产商、报关口岸等字段，检测公章，按审核规则生成 MD 和 JSON 审核报告，并支持 CLI 和对话交互触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[njkahn](https://clawhub.ai/user/njkahn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Trade operations teams, compliance reviewers, and developers use this skill to pre-audit import/export license document packages by extracting fields from PDFs or images, checking stamps, comparing documents against configured rules, and producing structured review reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic dependency installation can modify the host system. <br>
Mitigation: Install and run only in a controlled or disposable environment, and review installer commands before first execution. <br>
Risk: Sensitive trade or license document contents may be sent to an external LLM endpoint. <br>
Mitigation: Use only approved model endpoints and credentials, avoid highly sensitive documents unless approved, and clean generated reports, extracted files, temporary OCR data, and cached model configuration after use. <br>
Risk: Audit results can be incomplete or incorrect and may require business or compliance judgment. <br>
Mitigation: Treat generated pre-audit findings as review support and require human review before relying on pass, fail, or manual-review recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/njkahn/license-pre-audit) <br>
- [audit-rules.json](references/audit-rules.json) <br>
- [doc-types.json](references/doc-types.json) <br>
- [settings.json](references/settings.json) <br>
- [audit-rules.md](src/prompts/audit-rules.md) <br>
- [extract-fields.md](src/prompts/extract-fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Files, Shell commands] <br>
**Output Format:** [Markdown table and JSON audit report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped audit-result JSON and Markdown files under the configured reports directory and can print the Markdown table to stdout.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
