## Description: <br>
Kami Package Detection helps agents configure and run RTSP camera package monitoring with YOLO-World ONNX, structured alarm output, and notification options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13681882136](https://clawhub.ai/user/13681882136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor configured RTSP camera feeds for packages, parcels, and bags, then receive structured alarms or notifications when a new or moved package is detected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera snapshots or notification attachments may expose private camera imagery outside the local device. <br>
Mitigation: Review notification settings before use, disable image attachments or external image upload fallbacks when camera privacy matters, and confirm where snapshots are stored or sent. <br>
Risk: RTSP camera credentials embedded in URLs may be exposed through logs, process listings, or device-listing output. <br>
Mitigation: Use least-privilege camera credentials, avoid sharing logs that include RTSP URLs, and rotate camera passwords if exposure is suspected. <br>
Risk: Setup downloads dependencies and model assets, and evidence warns that optional privileged setup steps should be reviewed. <br>
Mitigation: Review setup.sh and configuration before installing, pin or audit dependencies where possible, and run privileged commands only after confirming they are needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/13681882136/kami-package-detection) <br>
- [Publisher profile](https://clawhub.ai/user/13681882136) <br>
- [KamiClaw privacy policy](https://kamiclaw-skill.kamihome.com/privacy) <br>
- [YOLO-World ONNX model archive](https://publicfiles.xiaoyi.com/kami-package-detection.zip) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON configuration examples, and runtime JSON alarm output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, RTSP camera access, and user-provided notification credentials when notifications are enabled.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
