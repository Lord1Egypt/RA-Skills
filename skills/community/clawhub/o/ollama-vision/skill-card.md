## Description:

Ollama Vision analyzes local image files with Ollama's qwen3-vl:4b model for image description, OCR, and custom information extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzm2023](https://clawhub.ai/user/lzm2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route selected images to a local Ollama vision model and receive descriptions, OCR text, or prompted extraction results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are sent to the user's local Ollama service for analysis.

Mitigation: Run Ollama only in a trusted local environment and avoid using the skill on sensitive images unless local service access is controlled.

Risk: Compressed temporary image files may be unsuitable for sensitive images in multi-user environments.

Mitigation: Avoid sensitive images in shared environments until temporary-file handling uses unique private files.

Risk: First use may trigger a qwen3-vl:4b model download of about 2-3GB.

Mitigation: Confirm bandwidth, storage, and operational approval before first use or pre-install the model.

Risk: Prompts and user-facing messages are Chinese-only.

Mitigation: Confirm the deployment audience can review and operate Chinese-language prompts and diagnostics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lzm2023/skills/ollama-vision)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text image analysis, OCR text, extraction results, or environment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May compress large images before analysis; first use may download the qwen3-vl:4b model locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
