## Description:

视频去水印解析 Skill，支持 20+ 平台短视频去水印解析，包括抖音、快手、小红书、微博、西瓜视频、豆包、云雀、B站等。

This skill is for research and development only.

## Publisher:

[mackjosn](https://clawhub.ai/user/mackjosn)

### License/Terms of Use:

MIT-0

## Use Case:

Users ask an agent to parse supported short-video and social-media links, then receive parser output for watermark-free video or media downloads. The skill can also start a local HTTP service for the same parsing workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download and run an unverified closed-source native program from a mutable Gitee branch.

Mitigation: Install only if the publisher and Gitee source are trusted; prefer a version with pinned releases, published hashes or signatures, and explicit confirmation before download.

Risk: The optional HTTP service may expose parser behavior on a local port if run without review.

Mitigation: Review the service binding and port behavior before running it, and keep access limited to localhost unless broader exposure is intentionally approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mackjosn/skills/parse-video-nomark)
- [Gitee repository](https://gitee.com/qiushuihanjing/parse-video-nomark)
- [Gitee binary distribution path](https://gitee.com/qiushuihanjing/parse-video-nomark/raw/master/dist/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text from shell commands, including parsed media links or local service status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download a platform-specific native binary before producing parser output.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
