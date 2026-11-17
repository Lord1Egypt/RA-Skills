## Description:

Image to Markdown - extract text from images (PNG, JPG, WebP) to Markdown with OCR. Use when reading text from screenshots, photos, scanned pages, or any image file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extract text from screenshots, photos, scanned pages, and other image files into Markdown using the MinerU Open API CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are uploaded to MinerU's cloud OCR service for processing.

Mitigation: Do not use the skill for highly sensitive images unless the cloud processing and retention behavior meet the user's data handling requirements.

Risk: The skill requires installing the mineru-open-api CLI from a package registry or Go module source.

Mitigation: Install from trusted registries, pin or review the package version where possible, and scan the dependency before deployment.

Risk: OCR output can be incomplete or incorrect, especially for low-quality images or mismatched language settings.

Mitigation: Review extracted Markdown against the source image and pass an explicit language hint when the default is not appropriate.

## Reference(s):

- [Img2md on ClawHub](https://clawhub.ai/tanis90/skills/img2md)
- [MinerU](https://mineru.net)
- [MinerU CLI](https://mineru.net/ecosystem?tab=cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR output depends on image quality, language hints, the 10MB image limit, and MinerU cloud API availability.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
