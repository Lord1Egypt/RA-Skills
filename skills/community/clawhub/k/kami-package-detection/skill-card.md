## Description: <br>
Kami Package Detection continuously monitors RTSP camera streams for packages, parcels, and bags with YOLO-World ONNX and alerts only when a new or moved package appears. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13681882136](https://clawhub.ai/user/13681882136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and smart-home operators use this skill to monitor configured RTSP camera feeds for package deliveries, doorway parcels, reception items, or warehouse cargo. The skill can run foreground checks or background monitoring and emits structured detection results for integration with notifications or other automations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Continuous camera monitoring may process sensitive household, office, or warehouse footage. <br>
Mitigation: Use only cameras and locations where monitoring is authorized, keep RTSP access scoped to the intended device, and stop the background detector when monitoring is not needed. <br>
Risk: Alert snapshots and logs can retain local paths, camera URLs, and image evidence after a detection. <br>
Mitigation: Restrict permissions on the skill directory, avoid embedding RTSP passwords in URLs where possible, and clear snapshots and logs on a regular schedule. <br>
Risk: Notification integrations can send alert data and possibly snapshot images to external services. <br>
Mitigation: Configure Feishu, Telegram, or Discord credentials only when required, verify the destination channels, and remove unused webhook or bot tokens from config. <br>
Risk: Setup downloads a model archive and may install additional packages during fallback export. <br>
Mitigation: Review installer behavior before execution, run setup in an isolated environment, and verify downloaded model files when operating in sensitive deployments. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/13681882136/kami-package-detection) <br>
- [Pre-built ONNX archive](https://publicfiles.xiaoyi.com/kami-package-detection.zip) <br>
- [Kami skill privacy policy](https://kamiclaw-skill.kamihome.com/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON alarm output from the detection script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Alarm JSON may include detected class, confidence, camera name, frame number, snapshot path, and bounding boxes; setup and runtime commands may create local files such as a virtual environment, model files, logs, and snapshots.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
