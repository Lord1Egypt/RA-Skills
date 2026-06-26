## Description: <br>
This skill controls JFTech PTZ camera one-key video masking by enabling, disabling, or checking privacy mode so the camera turns to a masked position and stops or resumes preview and recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to control privacy masking on supported, bound, online JFTech PTZ cameras for home, meeting-room, or scheduled privacy workflows. <br>

### Deployment Geography for Use: <br>
China, Asia, Europe, and North America <br>

## Known Risks and Mitigations: <br>
Risk: Enable, disable, and toggle actions can move the camera and stop or resume recording. <br>
Mitigation: Require explicit user confirmation before running actions that change masking state, camera position, preview, or recording. <br>
Risk: Signed device-control requests are sent to a configurable endpoint. <br>
Mitigation: Set JF_ENDPOINT only to an official documented JFTech regional host and review the endpoint before execution. <br>
Risk: The skill depends on JF_* credentials and device tokens. <br>
Mitigation: Keep credentials private, supply them through environment variables or a secure secret store, and rotate device tokens when exposure is suspected. <br>


## Reference(s): <br>
- [JFTech Open Platform Documentation](https://docs.jftech.com) <br>
- [ClawHub skill listing](https://clawhub.ai/jftech/jf-open-pro-video-masking) <br>
- [Publisher profile](https://clawhub.ai/user/jftech) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JFTech account, device, token, and regional endpoint configuration before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
