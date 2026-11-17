## Description:

Converts document images containing text, formulas, titles, and figures into structured code-style output with title markers, body lines, LaTeX formula calls, and image placeholders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-automation users can use this skill to convert screenshots or scanned document images into formatted output for downstream document generation workflows. It is especially oriented toward Chinese technical documents with headings, body text, formulas, and chart placeholders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default OCR path may send complete images to Baidu OCR using embedded shared credentials.

Mitigation: Use the default path only when third-party OCR processing is approved; otherwise configure a local-only OCR engine and replace embedded credentials with securely supplied project credentials.

Risk: Confidential screenshots, personal data, credentials, source code, or regulated documents could be exposed during OCR processing.

Mitigation: Screen input images before processing and keep sensitive or regulated documents on approved local-only infrastructure.

Risk: OCR, formula conversion, and title detection can produce incorrect output, especially for complex formulas or low-quality images.

Mitigation: Manually review formulas, headings, and key values before using generated output in documents or code workflows.

Risk: Unpinned dependencies can change behavior or introduce supply-chain risk.

Mitigation: Pin dependencies, install from trusted indexes, and scan the environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/image-to-code)
- [Baidu AI Console](https://console.bce.baidu.com/ai/)
- [Tesseract OCR documentation](https://tesseract-ocr.github.io/)
- [pytesseract API](https://github.com/madmaze/pytesseract)
- [OpenCV documentation](https://docs.opencv.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or UTF-8 text files containing PHP-style $word lines, LaTeX formula strings, and Markdown image placeholders.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on OCR engine availability, image quality, and manual review of formulas and headings.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
