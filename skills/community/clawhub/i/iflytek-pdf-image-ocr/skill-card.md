## Description:

Iflytek Pdf Image Ocr helps agents run iFlytek image and PDF OCR workflows to extract text from images and convert PDF documents to Word, Markdown, or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflytek.skills](https://clawhub.ai/user/iflytek.skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users can use this skill to OCR screenshots, scanned images, and PDF documents with iFlytek cloud OCR services. It is suited for extracting text, preserving document layout, and producing Word, Markdown, or JSON outputs from supported inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images and PDFs are sent to iFlytek cloud OCR services for processing.

Mitigation: Use the skill only with documents approved for third-party cloud processing, especially for confidential, regulated, client, or personal data.

Risk: PDF URL mode can also upload a local PDF, so a local document may be sent when the user expected URL-only processing.

Mitigation: Review command arguments before execution and avoid --pdf-url until the skill enforces a true file-or-URL choice.

Risk: OCR results and generated download URLs may expose document text or processed files.

Mitigation: Handle outputs as sensitive when source documents are sensitive, and avoid sharing generated links outside approved workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iflytek.skills/skills/iflytek-pdf-image-ocr)
- [iFlytek OCR service homepage](https://www.xfyun.cn/services/ocr)
- [iFlytek image OCR API documentation](https://www.xfyun.cn/doc/words/image_word_recognition/API.html)
- [iFlytek OCR service console](https://console.xfyun.cn/services/se75ocrbm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [CLI guidance and OCR results as plain text, Markdown, JSON, or Word download URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, requests, and iFlytek credentials through IFLY_APP_ID, IFLY_API_KEY, and IFLY_API_SECRET.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
