## Description: <br>
iClick Automation helps agents monitor and control connected no-jailbreak iOS devices through device status checks, screenshots, touch actions, text input, app actions, and media operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Undefined-Token](https://clawhub.ai/user/Undefined-Token) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect connected iOS device state and perform supervised automation tasks such as screenshots, tapping, swiping, text entry, app actions, and media handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over connected iOS devices, including touch, text entry, app actions, and media operations. <br>
Mitigation: Require manual confirmation for device-control actions and verify the target deviceId before every command. <br>
Risk: Screenshots and device metadata may expose private messages, credentials, tokens, photos, IP addresses, or device names. <br>
Mitigation: Use test devices or low-risk accounts first, treat screenshots as sensitive, and avoid sharing raw screenshots or device identifiers unless necessary. <br>
Risk: Media deletion and clearing actions can remove device-side files. <br>
Mitigation: Require explicit user confirmation before destructive media commands and confirm the file name or clear operation target. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Undefined-Token/iclick-skill) <br>
- [iClick website](https://iosclick.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell command examples; command execution returns JSON and may create temporary screenshot files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and access to connected iClick-compatible iOS devices.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
