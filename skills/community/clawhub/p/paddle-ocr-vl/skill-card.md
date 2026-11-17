## Description:

PaddleOCR-VL provides GPU-accelerated document parsing and OCR that detects layout and recognizes Chinese and English text, tables, charts, seals, vertical classical Chinese text, modern newspaper layouts, and mixed-content documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessy-huang](https://clawhub.ai/user/jessy-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to run OCR on local images, screenshots, newspaper pages, classical text, and mixed-content documents through a PaddleOCR-VL MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs unverified Docker images with broad local-file access and host networking.

Mitigation: Use only non-sensitive files and only when the container publisher and registry are trusted; prefer pinned image digests, no host networking, non-root execution, and a read-only staged input mount.

Risk: The security evidence reports a filename injection bug.

Mitigation: Use controlled filenames until the issue is fixed; update the skill to pass image paths safely instead of embedding filenames into executable Python source.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jessy-huang/skills/paddle-ocr-vl)
- [Publisher Profile](https://clawhub.ai/user/jessy-huang)
- [Project Homepage](https://github.com/user/paddle-ocr-vl-skill)
- [PaddleOCR-VL Documentation](https://www.paddleocr.ai/latest/version3.x/pipeline_usage/PaddleOCR-VL.html)
- [PaddleOCR-VL NVIDIA Blackwell Documentation](https://www.paddleocr.ai/latest/version3.x/pipeline_usage/PaddleOCR-VL-NVIDIA-Blackwell.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown setup guidance and JSON-formatted OCR or environment-check results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker, python3, nvidia-smi, NVIDIA GPU drivers, and local image paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
