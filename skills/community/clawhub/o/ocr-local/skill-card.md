## Description:

Extract text from images using Tesseract.js OCR (100% local, no API key required). Supports Chinese (simplified/traditional) and English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaw555](https://clawhub.ai/user/shaw555)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to extract text from local images, screenshots, and documents in Simplified Chinese, Traditional Chinese, and English without using an OCR API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and first use can download npm packages and Tesseract language data from third-party sources.

Mitigation: Use environments that permit those downloads, or pin tesseract.js to a reviewed exact version, add a lockfile, and prefetch or vendor required language data for offline or restricted deployments.

Risk: OCR output may be inaccurate for handwritten, low-contrast, poorly lit, or unclear images.

Mitigation: Review extracted text before using it in downstream decisions, and prefer clear, high-contrast source images.

## Reference(s):

- [Tesseract.js Project](https://github.com/naptha/tesseract.js)
- [ClawHub Skill Page](https://clawhub.ai/shaw555/skills/ocr-local)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Plain text, or JSON containing recognized text, confidence scores, words, and bounding boxes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Language selection supports chi_sim, chi_tra, eng, and combined language codes; OCR quality depends on source image clarity.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
