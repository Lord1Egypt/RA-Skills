## Description: <br>
Generate images & videos with AIsa. Gemini 3 Pro Image (image) + Qwen Wan 2.6 (video) via one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIsaDocs](https://clawhub.ai/user/AIsaDocs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate images and videos through AIsa APIs with one API key, including Gemini image generation and asynchronous Wan 2.6 video tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image URLs, and bearer-authenticated requests are sent to AIsa. <br>
Mitigation: Use a revocable API key where possible and avoid confidential prompts or private image URLs. <br>
Risk: Generated media downloads may overwrite chosen output paths or create large local files. <br>
Mitigation: Choose output paths deliberately and review generated file size and contents before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIsaDocs/openclaw-aisa-llm-image-video) <br>
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [Gemini GenerateContent API](https://aisa.mintlify.app/api-reference/chat/chat-api/google-gemini-chat.md) <br>
- [Video Generation API](https://aisa.mintlify.app/api-reference/aliyun/video/video-generation.md) <br>
- [Video Task Status API](https://aisa.mintlify.app/api-reference/aliyun/video/task.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell commands and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can save generated images and downloaded videos to local output files when the user runs the provided client commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
