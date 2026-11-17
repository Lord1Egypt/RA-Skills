## Description:

将论文 PDF 批处理为中文精读总结报告的工作流技能，支持通过 PaddleOCR 或 pdfplumber 抽取文本并调用配置的大模型生成报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mxingchtongaelofficial2568](https://clawhub.ai/user/mxingchtongaelofficial2568)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to batch-process paper PDFs into Chinese close-reading reports. It extracts PDF text locally with pdfplumber or optionally through a configured PaddleOCR endpoint, then sends the extracted text to a configured OpenAI-compatible summarizer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured OCR or LLM providers can receive PDF contents and extracted text.

Mitigation: Use only user-approved endpoints, prefer internal or self-hosted providers for confidential documents, and remove unused provider configuration.

Risk: The optional PaddleOCR path can fetch an unvalidated remote result URL returned by the OCR service.

Mitigation: Keep PaddleOCR disabled unless the endpoint is trusted, and validate OCR result URLs before treating the skill as low-risk.

Risk: Python dependencies can change behavior over time when installed from broad version ranges.

Mitigation: Install dependencies in an isolated environment and pin versions before production use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown reports and concise shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates one *_研读报告.md file per input PDF; token-like values should be redacted from logs and errors.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
