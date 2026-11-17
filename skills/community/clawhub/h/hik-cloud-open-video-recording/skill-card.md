## Description:

调用海康云眸开放平台视频云录制能力，帮助管理云录制项目、转码录制任务、录制文件、项目流量、资源上传和视频剪辑。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hik-cloud-open](https://clawhub.ai/user/hik-cloud-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run Hik-Cloud video recording workflows through an agent, including project administration, recording and frame extraction tasks, file lookup and download, traffic limits, uploads, and video clipping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Hik-Cloud credentials and can perform destructive or production-impacting actions.

Mitigation: Review before installation, use only trusted HTTPS Hik-Cloud base URLs, and require explicit human confirmation before delete, stop, flow-limit, upload, download-link, or clipping actions.

Risk: Bearer tokens or cached credentials could be exposed on shared systems.

Mitigation: Avoid passing bearer tokens on the command line and protect or disable the token cache when using shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hik-cloud-open/skills/hik-cloud-open-video-recording)
- [Publisher profile](https://clawhub.ai/user/hik-cloud-open)
- [Authentication reference](references/auth.md)
- [Video recording reference](references/video-recording.md)
- [Hik-Cloud video recording API documentation](https://pic.hik-cloud.com/opencustom/apidoc/online/open/b6f980108b8242258716079c118d5702.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a bundled Python helper that returns text summaries or structured JSON responses from Hik-Cloud APIs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
