## Description:

Human Avatar helps agents create talking portrait videos, full-body animations, text-to-image and image-to-video outputs, Qwen text-to-speech audio, and LingMou template avatar videos using Alibaba Cloud DashScope and LingMou APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davideuler](https://clawhub.ai/user/davideuler)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate avatar media, speech audio, image assets, and short videos through Alibaba Cloud-backed workflows. It is suited for creating talking-head videos, template digital-human broadcasts, full-body motion videos, and image-to-video sequences from prompts or local media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Alibaba Cloud credentials and personal media for cloud generation and OSS upload.

Mitigation: Use least-privilege Alibaba credentials, isolate the runtime, and install only when the selected prompts and media can be sent to Alibaba Cloud services and the user's OSS bucket.

Risk: Endpoint override variables and LingMou template-copy behavior can affect where requests go and mutate the user's Alibaba Cloud account resources.

Mitigation: Do not set endpoint override variables unless they are fully controlled, and review public-template copy behavior before using the skill on production accounts.

Risk: Generated video, speech, and avatar media can be mistaken for real human likeness or speech.

Mitigation: Use consented source media, disclose synthetic output where appropriate, and review generated media before publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davideuler/skills/human-avatar)
- [LivePortrait API](https://help.aliyun.com/zh/model-studio/liveportrait-api)
- [Text-to-Image V2 API](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)
- [Image-to-Video API](https://help.aliyun.com/zh/model-studio/image-to-video-api-reference/)
- [Qwen TTS Realtime](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime)
- [AnimateAnyone Detect API](https://help.aliyun.com/zh/model-studio/animate-anyone-detect-api)
- [AnimateAnyone Template API](https://help.aliyun.com/zh/model-studio/animate-anyone-template-api)
- [AnimateAnyone Video Generation API](https://help.aliyun.com/zh/model-studio/animateanyone-video-generation-api)
- [EMO API Reference](references/emo-api.md)
- [LingMou API Reference](references/lingmou-api.md)
- [OSS Upload Reference](references/oss-upload.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may result in generated media files, signed URLs, or downloaded audio/video/image artifacts when the referenced scripts are executed.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
