## Description:

抖音视频解析下载工具。从分享链接提取无水印下载地址，支持下载、转文字和内容分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kk-kingkong](https://clawhub.ai/user/kk-kingkong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to parse Douyin share links, retrieve watermark-free download URLs, download videos, transcribe audio with Whisper, and analyze video content through the configured douyin-analyzer MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on separately installed douyin-analyzer MCP code that is not bundled or pinned in the artifact.

Mitigation: Verify, scan, and pin the local douyin-analyzer MCP implementation before installing or running this skill.

Risk: Douyin share links may be sent to Douyin and the third-party liuxingw.com parsing service.

Mitigation: Do not process private or sensitive links unless sharing them with those services is acceptable.

Risk: Downloaded videos and generated transcripts may remain in /tmp after use.

Mitigation: Delete temporary video, audio, and transcript files when processing is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kk-kingkong/skills/kk-douyin-download)
- [ClawHub publisher profile](https://clawhub.ai/user/kk-kingkong)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local /tmp video or transcript files and a separately installed douyin-analyzer MCP server.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
