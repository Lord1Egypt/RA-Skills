## Description: <br>
A robust, permission-friendly method to capture macOS screens via OpenClaw screen.record. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taozhe6](https://clawhub.ai/user/taozhe6) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to capture a macOS screen by recording a short OpenClaw screen.record clip and extracting a PNG frame for inspection or reply attachment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots can capture sensitive visible information from the user's Mac screen. <br>
Mitigation: Before running the capture command, hide sensitive windows or messages and grant Screen Recording permission intentionally. <br>
Risk: The workflow depends on ffmpeg for frame extraction. <br>
Mitigation: If ffmpeg is missing, ask before installing it and use only a trusted source. <br>
Risk: A sleeping or locked display can produce a black frame instead of useful screen content. <br>
Mitigation: Ask the user to wake or unlock the screen before retrying the capture. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taozhe6/mac-node-snapshot) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, files] <br>
**Output Format:** [Markdown with inline bash commands and local file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a short MP4 intermediary and extracts a PNG screenshot at {skill}/tmp/snap.png.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
