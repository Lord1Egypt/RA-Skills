## Description:

Generate images and videos with AIsa using Gemini 3 Pro Image for image generation and Qwen Wan 2.6 for asynchronous video generation through one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to generate image and video assets through AIsa, including image prompts, Wan 2.6 video task creation, task polling, and optional media download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and image URLs are sent to AIsa.

Mitigation: Use only prompts and image URLs that are acceptable to share with AIsa.

Risk: The AISA_API_KEY is required for API access.

Mitigation: Store the key securely and avoid exposing it in shared logs, prompts, shell history, or generated files.

Risk: The optional video download can fetch an unvalidated provider-returned URL and write unlimited data to disk.

Mitigation: Avoid --download unless the returned media URL is trusted and the environment can tolerate a large file write.

Risk: Running the Python client in sensitive networks or low-storage environments may increase operational risk.

Mitigation: Review the skill before installation and run it only in environments where outbound API calls and media file writes are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xjordansg-yolo/skills/openclaw-aisa-image-video-models-wan2-6-gemini-3-pro-image-nano-banana)
- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa Gemini GenerateContent documentation](https://aisa.mintlify.app/api-reference/chat/chat-api/google-gemini-chat.md)
- [AIsa video generation documentation](https://aisa.mintlify.app/api-reference/aliyun/video/video-generation.md)
- [AIsa video task documentation](https://aisa.mintlify.app/api-reference/aliyun/video/task.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance, Files]

**Output Format:** [Markdown guidance with bash and Python command examples; optional JSON API responses and generated image or video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY. The Python client can save generated images locally, poll asynchronous video tasks, and optionally download returned video media.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
