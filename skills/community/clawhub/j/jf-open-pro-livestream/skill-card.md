## Description:

杰峰设备直播预览技能（开发版）。支持多端集成实时视频播放，兼容 HLS、RTSP、RTMP、FLV、MP4、WebRTC 等主流协议，适配 H.264/H.265 设备。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating JFTech devices use this skill to request signed livestream playback URLs for web, mobile app, WeChat mini-program, H5, or third-party player preview flows.

### Deployment Geography for Use:

China Mainland, Asia, Europe, and North America, using the JFTech regional API endpoints documented in the artifact.

## Known Risks and Mitigations:

Risk: The skill handles JFTech application secrets, device tokens, device passwords, and generated livestream URLs.

Mitigation: Use it only with JFTech devices and accounts you control, store credentials as private environment variables, and avoid sharing generated livestream URLs.

Risk: The configured API endpoint can send camera and device secrets to a host outside the documented JFTech domains.

Mitigation: Keep JF_ENDPOINT on the documented JFTech regional domains unless destination validation is added and reviewed.

Risk: The test-url action contacts the generated livestream URL with an HTTP HEAD request.

Mitigation: Avoid test-url on sensitive networks unless URL destination validation is added.

## Reference(s):

- [JFTech Open Platform documentation](https://docs.jftech.com)
- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-livestream)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text containing a livestream URL, status messages, and player-specific usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script can generate livestream URLs and optionally test a generated URL with an HTTP HEAD request.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
