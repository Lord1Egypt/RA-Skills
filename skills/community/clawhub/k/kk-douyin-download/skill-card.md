## Description: <br>
抖音视频解析下载工具，从分享链接提取无水印下载地址，支持下载、转文字和内容分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kk-kingkong](https://clawhub.ai/user/kk-kingkong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to parse Douyin share links, retrieve no-watermark video download links, download media, transcribe audio, and analyze video content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced local douyin-analyzer MCP server is not included in this package, so its behavior cannot be reviewed from the artifact alone. <br>
Mitigation: Verify that the local MCP server installation is trusted before using the skill. <br>
Risk: Douyin links, downloaded media, and transcription inputs may pass through the disclosed parsing and local media-processing workflow. <br>
Mitigation: Only process links and media that are acceptable for that workflow and avoid sensitive content. <br>
Risk: Temporary video, audio, or transcript files may remain under /tmp after use. <br>
Mitigation: Delete temporary files from /tmp when processing is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kk-kingkong/kk-douyin-download) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a local douyin-analyzer MCP server, ffmpeg, Whisper, and temporary files under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
