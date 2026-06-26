## Description: <br>
Supports JFTech camera image orientation tasks, including querying and setting horizontal mirror and vertical flip configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect or change image flip and mirror settings for bound, online JFTech camera devices through the JFTech OpenAPI. <br>

### Deployment Geography for Use: <br>
China, Asia, Europe, and North America <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change a camera's saved image orientation configuration. <br>
Mitigation: Use it only with devices you own or administer, verify the target device and channel before changing settings, and use the reset action when the intended orientation is not achieved. <br>
Risk: Credentials and device tokens are used for device-control API calls, and an unexpected endpoint could expose them. <br>
Mitigation: Keep JF_APP_SECRET and JF_DEVICE_TOKEN tightly scoped and rotated, and use only documented JFTech regional endpoints. <br>
Risk: When current camera configuration is missing, the script can fall back to a default Camera.Param payload before writing changes. <br>
Mitigation: Review the current device configuration before writes, and consider modifying the script to fail instead of writing defaults when Camera.Param is absent. <br>


## Reference(s): <br>
- [JFTech Open Platform documentation](https://docs.jftech.com) <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-device-image-flip) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jftech) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JFTech account, application credentials, device token, device serial number, and an online bound device.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
