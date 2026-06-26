## Description: <br>
Detect unregistered faces loitering in sensitive areas across one or many RTSP cameras using shared ONNX face detection and recognition models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13681882136](https://clawhub.ai/user/13681882136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operators and smart-home administrators use this skill to monitor authorized camera feeds for unknown people who remain in sensitive areas beyond a configured threshold. The skill can configure monitoring inputs, launch the detector, and route alerts through local JSON records and optional chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs face-recognition monitoring and stores biometric reference data and alert snapshots. <br>
Mitigation: Install and run it only with authority and consent for the cameras involved; define retention and deletion rules for face_db, alerts, logs, and related outputs. <br>
Risk: Alert delivery can send face snapshots or links to external services, including a public image-host fallback on the Feishu path when app credentials are absent. <br>
Mitigation: Prefer local-only operation or tightly controlled Feishu, Discord, or Telegram destinations; avoid the Feishu path without app credentials if public image upload is not acceptable. <br>
Risk: Configuration files and logs may contain sensitive camera URLs, webhooks, bot tokens, chat IDs, and biometric file paths. <br>
Mitigation: Restrict filesystem access to config.json, logs, face_db, and alerts; rotate exposed credentials and avoid sharing those files in support bundles. <br>
Risk: Dependencies and model downloads are retrieved during setup. <br>
Mitigation: Pin or verify dependencies and model artifacts before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/13681882136/kami-suspicious-person) <br>
- [Kami Suspicious Person privacy policy](https://kamiclaw-skill.kamihome.com/privacy) <br>
- [Model download package](https://publicfiles.xiaoyi.com/kami-suspicious-person-model.zip) <br>
- [uv installer referenced by setup](https://astral.sh/uv/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, json, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, persisted JSON configuration, and JSON alarm records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs continuously after launch and may emit repeated alarm JSON lines while monitoring camera streams.] <br>

## Skill Version(s): <br>
2.0.4 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
