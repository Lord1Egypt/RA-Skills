## Description: <br>
Human Avatar uses Alibaba Cloud DashScope and LingMou APIs to generate talking portrait videos, full-body animation, text-to-image images, image-to-video clips, and Qwen TTS speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davideuler](https://clawhub.ai/user/davideuler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to prepare avatar, portrait, animation, image, video, and speech generation workflows backed by Alibaba Cloud services. It helps agents select the right script, configure credentials and media requirements, and run generation commands for user-provided prompts and media. <br>

### Deployment Geography for Use: <br>
Global, subject to Alibaba Cloud service availability and region-specific API credentials. <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, videos, audio, text, and generated outputs may be sent to Alibaba Cloud services for processing. <br>
Mitigation: Use the skill only for media and prompts that are appropriate to process in Alibaba Cloud, and avoid submitting sensitive content unless that cloud processing is acceptable. <br>
Risk: Alibaba Cloud credentials and OSS signed URLs can expose user media if overprivileged or long lived. <br>
Mitigation: Use least-privilege credentials, a dedicated private OSS bucket or prefix, short signed-URL lifetimes, and lifecycle cleanup for temporary objects. <br>
Risk: Endpoint override variables can redirect traffic if configured to an untrusted destination. <br>
Mitigation: Do not set endpoint override variables unless the destination is explicitly trusted and reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/davideuler/human-avatar) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/davideuler) <br>
- [LivePortrait API](https://help.aliyun.com/zh/model-studio/liveportrait-api) <br>
- [Text-to-image API reference](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference) <br>
- [Image-to-video API reference](https://help.aliyun.com/zh/model-studio/image-to-video-api-reference/) <br>
- [Qwen TTS realtime API](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime) <br>
- [AnimateAnyone API reference](references/aa-api.md) <br>
- [EMO API reference](references/emo-api.md) <br>
- [LingMou API reference](references/lingmou-api.md) <br>
- [OSS upload reference](references/oss-upload.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated media file paths, and service result URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce images, videos, WAV audio, downloaded media files, signed OSS URLs, and task status messages from Alibaba Cloud services.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
