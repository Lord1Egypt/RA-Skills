## Description: <br>
Transform an Android phone with IP Webcam into an intelligent Edge AI security system with OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AliHmaou](https://clawhub.ai/user/AliHmaou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and home or small-site operators use this skill to configure an Android phone running IP Webcam for local motion monitoring, camera control, telemetry checks, and alert workflows. It is suited to frugal edge monitoring where raw frames stay local unless an alert-triggered frame is sent to AI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can involve remote access to a local phone camera and audio-capable IP Webcam server. <br>
Mitigation: Enable camera authentication where available, restrict network access, and avoid monitoring private areas without consent. <br>
Risk: Alert-triggered images may be sent to an AI service depending on the user's monitoring workflow. <br>
Mitigation: Decide in advance whether alert images may leave the local environment and review privacy requirements before enabling AI alerts. <br>
Risk: Continuous monitoring runner scripts obtained separately may affect privacy, network usage, or device behavior. <br>
Mitigation: Inspect separately obtained scripts before running them and monitor phone battery, Wi-Fi stability, and camera state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AliHmaou/ipwebcam) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, endpoint paths, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local IP Webcam access and command-line tools including compare, curl, and awk.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
