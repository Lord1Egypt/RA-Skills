## Description:

Generate images and videos with AIsa using Gemini 3 Pro Image and Qwen Wan 2.6 through one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:


## Use Case:

Developers, agents, content creators, and businesses use this skill to generate images and create, poll, and optionally download video generation tasks through the AIsa API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, and the AISA API key are sent to the AIsa API.

Mitigation: Use the skill only when AIsa is the intended media provider, keep AISA_API_KEY secret, and avoid private prompts or sensitive image URLs unless that handling is acceptable.

Risk: Generated image or video downloads may overwrite files at the selected output path.

Mitigation: Choose output filenames deliberately and avoid paths that contain important existing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/openclaw-aisa-llm-image-video-qwen-wan26-gemini-3-pro-image)
- [OpenClaw](https://openclaw.ai)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa llms.txt](https://aisa.mintlify.app/llms.txt)
- [Gemini GenerateContent documentation](https://aisa.mintlify.app/api-reference/chat/chat-api/google-gemini-chat.md)
- [AIsa video generation documentation](https://aisa.mintlify.app/api-reference/aliyun/video/video-generation.md)
- [AIsa video task documentation](https://aisa.mintlify.app/api-reference/aliyun/video/task.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown instructions with shell examples, Python client commands, JSON API responses, and generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, curl, and AISA_API_KEY; generated image or video downloads may write local output files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
