## Description:

Extract text from images using Tesseract.js OCR (100% local, no API key required). Supports Chinese (simplified/traditional) and English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15914355527](https://clawhub.ai/user/15914355527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract text from local image files, including screenshots and documents containing Simplified Chinese, Traditional Chinese, English, or mixed-language text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First use may download and cache Tesseract language data, which can affect reproducibility and offline operation.

Mitigation: Install and test the skill in the target environment ahead of use, and prefer pinned dependencies or a lockfile for stricter reproducibility.

Risk: OCR output may be incomplete or inaccurate for low-quality images, handwriting, or mismatched language settings.

Mitigation: Review extracted text before relying on it, and use JSON output confidence data when deciding whether manual verification is needed.

Risk: Input images and extracted text can contain sensitive information.

Mitigation: Treat both image files and OCR output as sensitive data according to the user's data-handling requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/15914355527/skills/ocr-local-v2)
- [Tesseract.js](https://github.com/naptha/tesseract.js)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [Plain text by default, or JSON with recognized text, confidence, words, and bounding boxes when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR quality depends on source image clarity, lighting, contrast, language selection, and Tesseract.js recognition confidence.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
