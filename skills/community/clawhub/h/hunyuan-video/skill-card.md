## Description:

腾讯混元生视频API - 支持文生视频、图生视频、视频风格化.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wszhhx](https://clawhub.ai/user/wszhhx)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to call Tencent Hunyuan video generation workflows for text-to-video, image-to-video, and video stylization tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tencent cloud credentials may be exposed or over-permissioned.

Mitigation: Use Tencent credentials scoped to the minimum required API access, inject secrets per session or through a secret manager, and avoid printing any part of SecretKey.

Risk: Prompts, media files, and media URLs are processed by Tencent Cloud.

Mitigation: Avoid submitting confidential media, internal URLs, or restricted content unless organizational policy permits Tencent Cloud processing.

Risk: The artifact includes unsafe TLS troubleshooting guidance.

Mitigation: Do not disable TLS verification; investigate certificate, proxy, or trust-store issues instead.

Risk: The skill depends on the Tencent Cloud Python SDK.

Mitigation: Install the SDK in an isolated environment and pin the package version according to local dependency-management policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wszhhx/skills/hunyuan-video)
- [Tencent Hunyuan Video API documentation](https://cloud.tencent.com/document/product/1616/107795)
- [Tencent Hunyuan Video console](https://hunyuan.cloud.tencent.com/#/app/videoModel)
- [Tencent Cloud API key management](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with CLI commands; execution can produce MP4 video files and JSON job metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, tencentcloud-sdk-python, TENCENT_SECRET_ID, and TENCENT_SECRET_KEY.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
