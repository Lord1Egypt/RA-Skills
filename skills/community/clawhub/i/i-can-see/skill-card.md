## Description: <br>
i-can-see lets an OpenClaw agent capture a photo from a configured ESP32-CAM and analyze the saved image when the user asks it to look. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[libaibuzai](https://clawhub.ai/user/libaibuzai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to capture a still image from a local ESP32-CAM, save it to a chosen path, and have the agent inspect the image before answering the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally captures photos from a camera and may record sensitive surroundings. <br>
Mitigation: Use it only with an ESP32-CAM you control, in spaces where camera capture is acceptable, and only when the user explicitly asks the agent to look. <br>
Risk: Saved snapshots may retain sensitive visual information after analysis. <br>
Mitigation: Store snapshots in a known folder and delete sensitive images after they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/libaibuzai/i-can-see) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance, Text] <br>
**Output Format:** [Markdown guidance with shell commands, saved JPEG image paths, and natural-language image observations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python requests and access to the configured local ESP32-CAM endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
