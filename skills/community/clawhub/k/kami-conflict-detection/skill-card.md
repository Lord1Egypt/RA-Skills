## Description: <br>
Real-time multi-camera physical conflict detection for RTSP camera streams or local video files using YOLO person pre-filtering and a remote multimodal Kami API for conflict analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13681882136](https://clawhub.ai/user/13681882136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and developers use this skill to configure and run continuous monitoring for physical fights, shoving, or scuffling across one or more RTSP cameras. It can also be run against local video files for testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive camera frames may leave the device for Kami analysis and configured alert destinations. <br>
Mitigation: Use only with appropriate privacy and legal controls for the monitored people and locations. <br>
Risk: The Feishu image fallback can upload snapshots to the public sm.ms image host. <br>
Mitigation: Prefer Feishu app upload, Discord or Telegram attachments, or a private image store instead of the public fallback. <br>
Risk: config.json can contain camera URLs, API keys, webhooks, bot tokens, and app secrets. <br>
Mitigation: Treat config.json as secret material, restrict file permissions, and avoid committing or sharing populated configuration. <br>
Risk: Setup downloads an installer path and model bundle before runtime. <br>
Mitigation: Verify the uv installer and model bundle, pin dependencies, and remove unused ultralytics before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/13681882136/kami-conflict-detection) <br>
- [Kami API registration](https://kamiclaw-skill.kamihome.com) <br>
- [YOLO ONNX model bundle](https://publicfiles.xiaoyi.com/kami-conflict-detection-model.zip) <br>
- [uv project](https://github.com/astral-sh/uv) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime JSON alert lines and saved media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires camera source configuration and a Kami API key; optional Feishu, Discord, and Telegram credentials enable push alerts.] <br>

## Skill Version(s): <br>
2.0.4 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
