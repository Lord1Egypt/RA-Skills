## Description:

Local speech-to-text workflow for configuring, testing, debugging, and validating an OpenAI-compatible STT server at `http://127.0.0.1:8000/v1`, including OpenClaw audio pipelines, multipart upload compatibility, model registration, streaming SSE behavior, response formats, local model-path fallback, and request routing checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mozi1924](https://clawhub.ai/user/mozi1924)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to isolate failures across a local speech-to-text server, OpenAI-style multipart transcription and translation endpoints, and OpenClaw audio routing. It helps distinguish backend, request-shape, model-registration, input-container, and client integration issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio files, transcripts, gateway logs, and proxy captures may contain sensitive speech content or metadata.

Mitigation: Use non-sensitive sample audio where possible, limit captures to the debugging window, and remove temporary logs or proxy dumps after analysis.

Risk: Less-common audio containers such as `.m4a` can fail before ASR quality is meaningfully tested.

Mitigation: Treat container failures as input compatibility issues and transcode suspect samples to `mp3` or `wav` before evaluating recognition quality.

Risk: Local STT implementations may only support a subset of OpenAI-compatible fields and streaming behavior.

Mitigation: Compare client requests against `references/stt-api.md` and the local OpenAPI schema before changing model or inference settings.

## Reference(s):

- [STT API calling document](references/stt-api.md)
- [Local OpenAPI schema](http://localhost:8000/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, API checks, and troubleshooting conclusions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands, endpoint checks, request-field comparisons, and risk-aware logging guidance.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
