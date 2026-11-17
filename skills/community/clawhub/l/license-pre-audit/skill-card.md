## Description:

进出口许可文档智能预审系统。支持 PDF 和图片处理：自动提取合同号、出口国、进口商、总金额、数量、重量、合格证编号、生产商、报关口岸等字段，检测公章，按审核规则执行审核，生成 MD 和 JSON 审核报告。支持 CLI 和对话交互两种方式触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[njkahn](https://clawhub.ai/user/njkahn)

### License/Terms of Use:

MIT-0

## Use Case:

Trade compliance and operations users can use this skill to pre-audit import and export license document packages. It extracts key fields from PDFs and images, checks configured rules, detects stamps, and returns audit findings for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install or modify runtime dependencies on the host.

Mitigation: Run it in a controlled environment and review dependency installation behavior before use on a primary machine.

Risk: Document text may be sent to an external LLM during field extraction.

Mitigation: Avoid confidential documents unless the configured LLM provider and data handling are acceptable for the document class.

Risk: LLM API credentials may be cached with weak protection.

Mitigation: Rotate any API key that may have been cached by this release and prefer short-lived or environment-provided credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/njkahn/skills/license-pre-audit)
- [Publisher Profile](https://clawhub.ai/user/njkahn)
- [Audit Rules Configuration](artifact/references/audit-rules.json)
- [Document Types Configuration](artifact/references/doc-types.json)
- [Runtime Settings](artifact/references/settings.json)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text]

**Output Format:** [Markdown table and structured JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved as timestamped audit-result Markdown and JSON files.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
