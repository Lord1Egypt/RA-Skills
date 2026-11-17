## Description:

Nano Banana 2 文生图 helps agents turn text prompts into AI Hive image-generation commands for product concepts, social content, educational illustrations, scene design, and creative variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, designers, and developers use this skill to draft text-only Nano Banana 2 image generation prompts, run AI Hive generation tasks, and converge on channel-ready concept images without uploading local reference assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI Hive API key and can store it locally.

Mitigation: Use a scoped, revocable API key and keep local configuration restricted to the documented 0600 permissions.

Risk: Text prompts are sent to AI Hive for image generation.

Mitigation: Avoid submitting confidential, regulated, or unapproved third-party content unless that use is authorized.

Risk: Generated media is downloaded from provider-returned result URLs without strong validation.

Mitigation: Use a dedicated output directory and review downloaded files before reuse or distribution.

Risk: Generated concept images may be mistaken for real products, real places, or documentary photos.

Mitigation: Label generated images as concepts and avoid presenting them as real-world evidence or production-ready assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-text-to-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses text prompts, optional batch count, routing mode, aspect-ratio parameters, and an output directory for generated image downloads.]

## Skill Version(s):

1.0.1 (source: server release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
