## Description:

Image to Markdown - extract text from images (PNG, JPG, WebP) to Markdown with OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract Markdown text from screenshots, document photos, scanned pages, and other supported image files through MinerU OCR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are uploaded to MinerU's cloud API for OCR, which can expose confidential, regulated, or private content.

Mitigation: Use only with images approved for cloud processing, and check MinerU terms and internal policy before processing sensitive material.

Risk: The skill depends on installing and running the third-party mineru-open-api CLI.

Mitigation: Install from a trusted channel, prefer pinned or verified releases when available, and review commands before execution.

Risk: OCR output can omit, misread, or reorder text from low-quality images.

Mitigation: Treat extracted Markdown as draft text and verify critical content against the source image.

## Reference(s):

- [Pic2md ClawHub Release](https://clawhub.ai/tanis90/skills/pic2md)
- [MinerU](https://mineru.net)
- [MinerU CLI Ecosystem](https://mineru.net/ecosystem?tab=cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MinerU Open API for OCR; flash-extract supports images up to 10MB.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
