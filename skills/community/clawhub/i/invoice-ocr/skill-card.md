## Description:

发票内容识别 helps agents process VAT invoice PDFs and common image formats, call Baidu Cloud OCR, extract key invoice fields, assess recognition quality, and produce a structured Excel report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengyulong](https://clawhub.ai/user/pengyulong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users can use this skill to recognize VAT invoice content from uploaded PDFs or images, batch process invoice files, and generate Excel summaries for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice images and extracted tax or business data are sent to Baidu Cloud OCR.

Mitigation: Use only invoices that may legally and contractually leave the processing environment.

Risk: The skill handles Baidu API credentials.

Mitigation: Keep credentials outside shared artifacts, rotate them regularly, and use a dedicated environment variable or .env workflow.

Risk: The documented installation command can modify system Python packages.

Mitigation: Run the skill in a dedicated virtual environment and pin dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pengyulong/skills/invoice-ocr)
- [Baidu Intelligent Cloud Console](https://console.bce.baidu.com/)
- [Baidu OCR Console](https://console.bce.baidu.com/ai/#/ai/ocr/overview/index)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an Excel invoice summary and concise processing status; requires Baidu OCR credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
