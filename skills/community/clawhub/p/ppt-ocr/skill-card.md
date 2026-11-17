## Description:

OCR for PowerPoint (.ppt, .pptx) presentations with scanned or image-embedded slides using MinerU to extract text from image-based presentation content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to OCR scanned or image-heavy PowerPoint presentations and convert extracted slide content into readable, searchable Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation content is processed through a third-party MinerU CLI and service.

Mitigation: Confirm MinerU/OpenDataLab and the mineru-open-api package are trusted before installation, and do not process confidential decks unless third-party OCR processing is acceptable.

Risk: Global package installation can introduce supply-chain and environment risk.

Mitigation: Prefer a pinned or isolated install and avoid running global installs with elevated privileges.

Risk: The skill requires a MinerU token for extraction workflows.

Mitigation: Provide the token through the documented MINERU_TOKEN environment variable or interactive auth flow, and avoid exposing credentials in shared logs or files.

## Reference(s):

- [Ppt Ocr on ClawHub](https://clawhub.ai/mzlzyca/skills/ppt-ocr)
- [MinerU](https://mineru.net)
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU)
- [mineru-open-api Go package](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mineru-open-api and a MINERU_TOKEN for extraction.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
