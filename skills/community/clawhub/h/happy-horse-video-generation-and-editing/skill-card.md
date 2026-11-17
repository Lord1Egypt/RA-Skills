## Description:

HappyHorse 视频生成与编辑 helps video editors, post-production teams, advertising producers, ecommerce teams, and creators generate or edit videos from text, images, video, or audio through AI Hive, with media upload, task tracking, and result download support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video production teams, ecommerce operators, and developers use this skill to submit HappyHorse text-to-video, image-to-video, reference-to-video, video-to-video, audio-to-video, and video editing jobs through AI Hive. It is intended for advertising, TVC, product showcase, social commerce, short drama, comic drama, and social media video production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and selected media may be sent to a configurable AI Hive endpoint.

Mitigation: Use a protected configuration file or environment secret for the API key, avoid passing secrets on the command line, and set a custom base URL only when the endpoint is trusted.

Risk: Broad activation keywords may cause the skill to be considered for competitor comparisons, ecommerce advice, or general AI video research.

Mitigation: Confirm the user intends to use AI Hive or HappyHorse video generation or editing before invoking the skill.

Risk: Video generation and batch use may incur cost, and local task timeouts do not necessarily mean remote generation failed.

Mitigation: Review runtime pricing before high-volume use, keep returned task IDs, and query existing tasks instead of resubmitting after a timeout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/happy-horse-video-generation-and-editing)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands; task status may be returned as JSON and generated media is downloaded as MP4, MOV, or another model-supported file format.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key; can upload selected media, submit generation tasks, poll task status, and download completed outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
