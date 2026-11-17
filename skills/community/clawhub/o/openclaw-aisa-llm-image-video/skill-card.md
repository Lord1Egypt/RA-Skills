## Description:

Generate images & videos with AIsa. Gemini 3 Pro Image (image) + Qwen Wan 2.6 (video) via one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to generate image files and manage asynchronous video generation tasks through the AIsa API using a single API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, and the AIsa API key are sent to AIsa services.

Mitigation: Install only if you trust AIsa with those inputs, keep the API key in AISA_API_KEY rather than command-line arguments, and avoid submitting sensitive prompts or URLs.

Risk: The video download mode retrieves a returned URL and writes it to the local filesystem.

Mitigation: Use a controlled output directory and avoid --download unless URL allowlisting, redirect checks, and file-size limits are acceptable for the deployment.

Risk: The security summary says API-key handling and video download network-safety gaps require review before installation.

Mitigation: Review the skill before deployment and add controls for URL allowlisting, redirect handling, and file-size limits where required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/openclaw-aisa-llm-image-video)
- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa API documentation index](https://aisa.mintlify.app/llms.txt)
- [Gemini GenerateContent API](https://aisa.mintlify.app/api-reference/chat/chat-api/google-gemini-chat.md)
- [Qwen Wan video generation API](https://aisa.mintlify.app/api-reference/aliyun/video/video-generation.md)
- [Video task polling API](https://aisa.mintlify.app/api-reference/aliyun/video/task.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and JSON API responses; generated media is saved as image or MP4 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; video generation uses asynchronous create, status, wait, and optional MP4 download commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
