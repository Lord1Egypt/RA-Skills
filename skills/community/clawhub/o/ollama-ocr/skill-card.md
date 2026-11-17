## Description:

Use Ollama's vision/OCR models to recognize text from images. Supports glm-ocr, llava, moondream, and llama3.2-vision models. Ideal when you need local offline OCR without relying on cloud APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extract text from screenshots, photos, receipts, and other images through locally hosted Ollama vision/OCR models. It is especially relevant when image content should stay within a trusted local environment instead of being sent to cloud OCR APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are sent to the configured Ollama HTTP endpoint rather than processed entirely inside the skill process.

Mitigation: Use the skill only after confirming that 172.17.0.2:11434 resolves to the intended trusted local Ollama instance in the deployment environment.

Risk: Highly sensitive images may be exposed if the configured Docker or network path is not trusted.

Mitigation: Avoid highly sensitive images unless the local Ollama service, container networking, and host access controls have been verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/skills/ollama-ocr)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Plain text OCR output with optional Python API usage and command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable local Ollama HTTP endpoint and a downloaded vision/OCR model.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
