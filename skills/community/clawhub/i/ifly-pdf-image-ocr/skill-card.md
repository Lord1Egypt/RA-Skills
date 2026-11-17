## Description:

ifly-pdf-image-ocr supports image OCR, PDF document recognition, PDF-to-Word or Markdown conversion, and structured OCR output through iFlytek cloud APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingzhe2020](https://clawhub.ai/user/qingzhe2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract text and document structure from images and PDFs, convert PDFs into Word, Markdown, or JSON outputs, and guide use of iFlytek OCR credentials and command-line scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, PDFs, or public PDF URLs selected by the user are sent to iFlytek's cloud OCR service for processing.

Mitigation: Use only documents whose confidentiality and data-handling requirements are compatible with the user's iFlytek account and terms.

Risk: The skill relies on API credentials and may display or store OCR output in local files or logs.

Mitigation: Keep IFLY_APP_ID, IFLY_API_KEY, and IFLY_API_SECRET protected, and avoid saving sensitive OCR results where unauthorized users can read them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingzhe2020/skills/ifly-pdf-image-ocr)
- [iFlytek Open Platform](https://console.xfyun.cn/)
- [iFlytek OCR service page](https://console.xfyun.cn/services/se75ocrbm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with shell commands and OCR outputs in text, Markdown, JSON, or Word-compatible document downloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires iFlytek API credentials; selected files or public PDF URLs are sent to iFlytek cloud OCR services.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
