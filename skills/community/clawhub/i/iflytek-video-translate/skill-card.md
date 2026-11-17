## Description:

Use when user asks to translate videos, dub video content, or localize videos into other languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflytek.skills](https://clawhub.ai/user/iflytek.skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and localization teams use this skill to submit video URLs to iFlytek/XFYUN for AI dubbing, language translation, task listing, and task-status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends XFYUN API credentials, video URLs, and task metadata to an iFlytek runtime endpoint.

Mitigation: Use approved XFYUN accounts, avoid shared or preconfigured credentials, and submit only videos that are permitted to leave the user's environment.

Risk: The documented API endpoint and coded runtime endpoint do not match.

Mitigation: Reconcile the endpoint against iFlytek/XFYUN documentation and organization policy before use.

Risk: The confirm_transcript action and force_rerun option can approve transcript content and continue processing without manual review.

Mitigation: Use confirm_transcript or force_rerun only when the user intentionally approves the transcript and wants processing to continue.

## Reference(s):

- [iFlytek/XFYUN Video Translation Documentation](https://www.xfyun.cn/doc/Develop/Video_Translation)
- [ClawHub Skill Page](https://clawhub.ai/iflytek.skills/skills/iflytek-video-translate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, XFYUN_API_KEY, and XFYUN_API_SECRET; task results may include translated video and subtitle URLs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
