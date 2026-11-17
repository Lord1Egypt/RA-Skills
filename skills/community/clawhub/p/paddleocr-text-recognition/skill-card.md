## Description:

Extracts machine-readable OCR text from images, screenshots, scans, and scanned PDFs, with line-level text and optional bounding boxes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobholamovic](https://clawhub.ai/user/bobholamovic)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent users use this skill to extract plain text from images, screenshots, photos, scans, and scanned PDFs through the PaddleOCR CLI. It is best suited for line-level OCR output and not for tables, formulas, charts, or complex document layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local images or PDFs may be sent to PaddleOCR's external API without a clear privacy confirmation.

Mitigation: Use only approved data with the external OCR service; avoid submitting secrets, regulated records, internal screenshots, or confidential documents unless that service is approved for that data.

Risk: Runtime dependency behavior can change if the PaddleOCR package is installed without controls.

Mitigation: Use a pinned dependency version or controlled runtime for higher-risk use.

Risk: OCR output may be incomplete or unsuitable for tables, formulas, charts, and complex document layouts.

Mitigation: Use a document parsing workflow for complex layouts and review OCR results before relying on them.

## Reference(s):

- [PaddleOCR Official CLI Documentation](https://www.paddleocr.ai/latest/en/version3.x/inference_deployment/serving/paddleocr_official_api/cli.html)
- [ClawHub Skill Page](https://clawhub.ai/bobholamovic/skills/paddleocr-text-recognition)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON OCR result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns complete extracted content when feasible; examples include line text, recognition scores, optional bounding boxes, page ranges, and saved JSON output.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
