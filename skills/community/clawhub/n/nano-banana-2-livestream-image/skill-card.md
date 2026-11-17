## Description:

This skill helps agents create livestream commerce image assets with Nano Banana 2 through AI Hive, including preview covers, livestream backgrounds, product explainer cards, promotion placeholders, and replay covers with UI safe areas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External livestream commerce operators, designers, and agent users use this skill to prepare Nano Banana 2 image-generation prompts and commands for broadcast covers, room backgrounds, product cards, promotion placeholders, and replay thumbnails. It emphasizes safe areas for live UI overlays and keeping time-sensitive prices, inventory, discounts, and platform policy details out of generated images until reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private or unreleased reference images may be uploaded to AI Hive or storage destinations returned by the service.

Mitigation: Use the skill only when AI Hive and its returned storage destinations are trusted, and avoid uploading sensitive or unreleased images.

Risk: Generated files are downloaded to a local output directory and may overwrite or expose material if a shared destination is used.

Mitigation: Use a disposable or dedicated output directory and review downloaded files before publishing or reusing them.

Risk: The browser-based initialization flow can associate the skill name with account activity.

Mitigation: Configure the API key manually when skill-identifying account telemetry is a concern.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-livestream-image)
- [AI Hive API](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI Hive image-generation tasks, poll task status, upload approved reference images, and download generated image files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
