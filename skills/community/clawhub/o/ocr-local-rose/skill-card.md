## Description:

Extract text from images using Tesseract.js OCR (100% local, no API key required). Supports Chinese (simplified/traditional) and English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roseknife520](https://clawhub.ai/user/roseknife520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to extract text from image files locally with Tesseract.js, including Simplified Chinese, Traditional Chinese, and English content. It can return plain text or JSON with confidence and word bounding boxes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: npm installation and first-run language model downloads introduce supply-chain and network-fetch exposure.

Mitigation: Pin and review dependency versions, use a trusted registry with the retained lockfile, and pre-download language data in stricter environments.

Risk: OCR results can be inaccurate for low-contrast, poorly lit, or handwritten images.

Mitigation: Review extracted text before relying on it and use clear, well-lit images with the intended language selection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roseknife520/skills/ocr-local-rose)
- [Tesseract.js](https://github.com/naptha/tesseract.js)
- [Simplified Chinese language data](https://cdn.jsdelivr.net/npm/@tesseract.js-data/chi_sim/4.0.0_best_int/chi_sim.traineddata.gz)
- [English language data](https://cdn.jsdelivr.net/npm/@tesseract.js-data/eng/4.0.0_best_int/eng.traineddata.gz)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON emitted by a Node.js CLI, with progress and errors on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON mode includes recognized text, confidence, words, and bounding boxes; OCR accuracy depends on image quality and selected language data.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
