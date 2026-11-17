## Description:

Extract text from images and PDFs using the GLM-OCR API, including table recognition, formula extraction, and handwriting recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredforreal](https://clawhub.ai/user/jaredforreal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use GLM-OCR to extract Markdown text from screenshots, scanned documents, photos, images, and PDFs through the GLM-OCR service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images, PDFs, or URLs are sent to the GLM-OCR service for processing.

Mitigation: Use the skill only for content approved for external OCR processing, and avoid submitting sensitive files unless the service and data handling are acceptable.

Risk: The ZHIPU_API_KEY credential is required and could be exposed if entered directly in shell history or committed in a .env file.

Mitigation: Store the key in an environment variable or protected .env file, keep it out of version control, and rotate it if exposure is suspected.

Risk: Dependency behavior can change over time because the artifact declares requests>=2.31.0.

Mitigation: Pin and review dependencies before deployment in stricter or production-controlled environments.

## Reference(s):

- [GLM-OCR skill homepage](https://github.com/zai-org/GLM-OCR/tree/main/skills/glmocr)
- [GLM-OCR GitHub repository](https://github.com/zai-org/GLM-OCR)
- [Output schema](references/output_schema.md)
- [BigModel API keys](https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [JSON envelope containing extracted Markdown text, layout details, source metadata, and error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; GLM_OCR_TIMEOUT is optional; CLI output can be printed or saved to a JSON file.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
