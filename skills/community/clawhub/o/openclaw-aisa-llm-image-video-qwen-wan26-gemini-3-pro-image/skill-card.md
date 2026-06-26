## Description: <br>
Generate images & videos with AIsa. Gemini 3 Pro Image (image) + Qwen Wan 2.6 (video) via one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIsaDocs](https://clawhub.ai/user/AIsaDocs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, AI agents, content creators, and businesses use this skill to generate images and videos through AIsa with one API key, including creating media files, starting video tasks, polling task status, and downloading completed videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image URLs, task IDs, and API usage are sent to AIsa. <br>
Mitigation: Install only if you trust AIsa and the publisher with this data, and review prompts and reference URLs before sending requests. <br>
Risk: API usage can consume paid quota or incur billing charges. <br>
Mitigation: Monitor AIsa billing or quota and choose generation settings such as duration and resolution deliberately. <br>
Risk: Passing the API key on the command line can expose it through shell history or process listings. <br>
Mitigation: Prefer the AISA_API_KEY environment variable over the --api-key command-line option. <br>
Risk: The --download option writes generated media to local paths. <br>
Mitigation: Use --download only with expected generated media and review the output path before writing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIsaDocs/openclaw-aisa-llm-image-video-qwen-wan26-gemini-3-pro-image) <br>
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [AIsa llms.txt](https://aisa.mintlify.app/llms.txt) <br>
- [Gemini GenerateContent documentation](https://aisa.mintlify.app/api-reference/chat/chat-api/google-gemini-chat.md) <br>
- [AIsa video generation documentation](https://aisa.mintlify.app/api-reference/aliyun/video/video-generation.md) <br>
- [AIsa task polling documentation](https://aisa.mintlify.app/api-reference/aliyun/video/task.md) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and Python client usage; generated media is saved as image or MP4 files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl, and AISA_API_KEY; video generation uses asynchronous tasks and optional local download.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
