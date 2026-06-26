## Description: <br>
MDClaw OpenClaw API 技能，支持文字转语音(TTS)、文生图(Text to Image)、文生视频(Text to Video)、图生视频(Image to Video)等多模态 AI 能力。通过网关服务统一调用，支持账号注册、图片上传、任务轮询等完整功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnskycn](https://clawhub.ai/user/cnskycn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call the MDClaw OpenClaw gateway for text-to-speech, image generation, video generation, image upload, search, weather, and web-summary workflows from an agent or Python client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, URLs, and account credentials are sent to the external MDClaw/appmiaoda service. <br>
Mitigation: Use a dedicated API key and password, and submit confidential images, private URLs, or sensitive text only when external processing is acceptable. <br>
Risk: Generated images, videos, audio, search answers, weather results, and web summaries depend on remote service responses. <br>
Mitigation: Review returned content and URLs before relying on them or sharing downloaded outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnskycn/mdclaw-openclaw) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and API call descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can guide agents to submit remote MDClaw API requests and handle returned URLs, task identifiers, status responses, downloaded files, or error messages.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
