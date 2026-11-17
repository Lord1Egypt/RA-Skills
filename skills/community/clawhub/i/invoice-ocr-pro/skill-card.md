## Description:

发票识别技能用于上传发票图片或文件进行 OCR 识别，并返回发票票面结构化信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxt](https://clawhub.ai/user/zxt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to upload invoice files and extract structured invoice fields such as invoice number, dates, amounts, buyer and seller details, and line items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends invoice files to skill.quandianfapiao.com for OCR processing.

Mitigation: Use only invoices the user is allowed to transmit to that service and review data handling requirements before processing sensitive documents.

Risk: The security review says the skill asks users to share an API key in chat and persistently writes it into shell configuration without clear consent or safe secret handling.

Mitigation: Use a platform secret manager or per-run environment variable, avoid pasting long-lived API keys into chat, and do not allow automatic modification of ~/.bashrc, ~/.zshrc, or persistent user environment settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxt/skills/invoice-ocr-pro)
- [Publisher profile](https://clawhub.ai/user/zxt)
- [ZXT invoice OCR service](https://skill.quandianfapiao.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with structured invoice fields and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports PDF, OFD, JPEG, JPG, PNG, and XML invoice files up to 10 MB; requires ZXT_API_KEY or an apiKey argument.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
