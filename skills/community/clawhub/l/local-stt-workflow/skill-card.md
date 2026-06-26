## Description: <br>
Local speech-to-text workflow for configuring, testing, debugging, or validating an OpenAI-compatible STT server, typically on http://127.0.0.1:8000/v1, including OpenClaw audio pipelines, multipart upload compatibility, model registration, streaming SSE behavior, response_format handling, local model-path fallback, and request-routing investigations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mozi1924](https://clawhub.ai/user/mozi1924) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure, test, and debug a local OpenAI-compatible speech-to-text server and its integration with OpenClaw audio pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands target a localhost STT service and may send audio samples to whichever server is listening on that port. <br>
Mitigation: Verify the local server is trusted before testing and use non-sensitive sample audio when possible. <br>
Risk: Less-common audio containers can fail before transcription and be mistaken for ASR quality issues. <br>
Mitigation: Transcode niche formats such as .m4a to mp3 or wav before judging recognition quality. <br>


## Reference(s): <br>
- [STT API reference](references/stt-api.md) <br>
- [Local OpenAPI schema](http://localhost:8000/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on local STT server checks, multipart request compatibility, response formats, streaming behavior, and OpenClaw routing diagnostics.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
