## Description:

Extract text from images using Tesseract.js OCR (100% local, no API key required). Supports Chinese (simplified/traditional) and English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nvoicejacob](https://clawhub.ai/user/nvoicejacob)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extract printed text from local image files, including Simplified Chinese, Traditional Chinese, English, and mixed-language images. It can return either plain text or JSON with confidence and word bounding boxes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may run npm package install behavior for Tesseract.js and its dependencies.

Mitigation: Install only after reviewing the package dependency chain, prefer the committed lockfile, and use an isolated environment for sensitive systems.

Risk: First use may download OCR language data even though the skill is described as local-only.

Mitigation: Preload approved language data in controlled environments and document the cache location before offline or restricted-network use.

Risk: The dependency declaration allows compatible Tesseract.js updates instead of pinning an exact package version.

Mitigation: Pin Tesseract.js to an exact reviewed version before deployment where reproducibility or supply-chain control is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nvoicejacob/skills/ocr-local-1-0-0)
- [Publisher profile](https://clawhub.ai/user/nvoicejacob)
- [Tesseract.js](https://github.com/naptha/tesseract.js)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON emitted by a local Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON output includes recognized text, overall confidence, words, per-word confidence, and bounding boxes.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact _meta.json, package.json, and PUBLISH.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
