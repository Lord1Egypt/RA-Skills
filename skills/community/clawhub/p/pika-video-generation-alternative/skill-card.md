## Description:

This skill helps agents turn Pika-style short-video and object-transformation requests into single-effect AI Hive Seedance 2.5 workflows for text-to-video, image-start animation, reference-rhythm borrowing, video editing, and extension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to plan and run single-effect AI video generation or editing through AI Hive Seedance 2.5. It focuses on preserving approved product or person identity, limiting each clip to one visible transformation, and avoiding Pika proprietary templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI Hive API key and can upload selected images or videos to AI Hive-controlled upload URLs.

Mitigation: Use a dedicated key in a sandboxed environment, avoid sensitive media, and upload only assets that are approved for the intended use.

Risk: The helper script gives the remote service substantial control over media upload destinations and generated download locations.

Mitigation: Set a specific output directory and review or patch the downloader before routine use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/pika-video-generation-alternative)
- [AI Hive API Endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline bash commands and JSON configuration examples; CLI runs may download MP4 video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key and may upload user-selected images or videos to AI Hive-controlled upload URLs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
