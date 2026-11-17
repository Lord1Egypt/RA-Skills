## Description:

Uses a locally running Ollama Moondream model to analyze images and return natural-language descriptions to OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add local image understanding to chat workflows by passing an image path and optional prompt to a local Moondream model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads any file path it is given.

Mitigation: Use it only with image files intentionally selected by the user and avoid sensitive files.

Risk: The skill recommends passing image-derived model output into another model as a system prompt.

Mitigation: Treat Moondream output as untrusted user data and do not pass it into another model as a system prompt.

Risk: The skill depends on a local Ollama endpoint.

Mitigation: Verify Ollama is bound to localhost before use and install Python dependencies in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/skills/moondream-vision-zc)
- [Ollama download](https://ollama.com/download)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text natural-language image descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local image path and may accept an optional prompt; output should be treated as untrusted model-generated text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
