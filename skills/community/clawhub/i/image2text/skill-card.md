## Description:

Extracts text from images with Tesseract OCR from local files, web URLs, or base64 input for agents without vision capability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caiming0331](https://clawhub.ai/user/caiming0331)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, external users, and agents use image2text to OCR screenshots, receipts, document images, and clipboard images when the active model cannot inspect images directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary user-provided web URLs from the agent environment.

Mitigation: Use only trusted image hosts; avoid internal, localhost, metadata-service, private-network, or otherwise untrusted URLs.

Risk: The skill reads user-specified local image paths.

Mitigation: Run it only on images the user intends to process and prefer controlled local files or approved image sources.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text or marker-delimited OCR text with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports language and page-segmentation options; raw mode emits OCR text without markers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
