## Description: <br>
使用小米 MiMo 的多模态模型分析和理解图片、视频和音频。当用户发送图片/视频/音频附件，询问视觉内容，请求图片描述、OCR、物体检测、场景理解、视频分析或音频转录/理解时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xcchenx345](https://clawhub.ai/user/xcchenx345) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to send image, video, audio, or mixed media inputs to Xiaomi MiMo for description, OCR, object detection, scene understanding, transcription, and related multimodal analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads submitted media, URLs, and prompts to a remote MiMo API endpoint. <br>
Mitigation: Use it only with media you are approved to send to Xiaomi MiMo, and avoid sensitive or regulated content unless your organization has approved that workflow. <br>
Risk: The scripts can read MiMo API credentials from environment variables or an OpenClaw configuration file. <br>
Mitigation: Prefer setting MIMO_API_KEY explicitly for this tool and review local credential configuration before running it. <br>
Risk: The API endpoint can be overridden, which could send media and credentials to a different destination. <br>
Mitigation: Do not set MIMO_API_ENDPOINT unless you intentionally trust that endpoint to receive both the media payload and API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xcchenx345/mimo-omni) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Plain text responses from the MiMo API, with usage diagnostics written to stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports image, multi-image, video, audio, and mixed video/audio inputs; local files may be base64-encoded and uploaded to the configured MiMo endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
