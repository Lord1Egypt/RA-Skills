## Description:

OCR document extraction - extract text from scanned documents, photos, and images using OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extract text from scanned PDFs, photographed pages, images, and handwritten notes through the MinerU Open API CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses a third-party CLI.

Mitigation: Install only in environments where the MinerU CLI is approved, and prefer a reviewed or pinned CLI version in controlled deployments.

Risk: Documents are uploaded to MinerU's cloud OCR service for processing.

Mitigation: Avoid sending confidential documents unless MinerU's privacy terms meet the user's requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tanis90/skills/ocr-document)
- [MinerU](https://mineru.net)
- [MinerU CLI Download](https://mineru.net/ecosystem?tab=cli)
- [mineru-open-api npm package](https://www.npmjs.com/package/mineru-open-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and OCR text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local files and URLs; documented limits are 10MB or 20 pages per document.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
