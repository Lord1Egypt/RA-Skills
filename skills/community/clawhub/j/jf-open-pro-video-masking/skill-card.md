## Description:

Controls the one-key privacy mask on supported JFTech PTZ cameras, moving the camera to its privacy position and disabling live preview and recording while masking is enabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to enable, disable, or check privacy masking on bound JFTech PTZ camera devices for home, meeting-room, or scheduled privacy workflows.

### Deployment Geography for Use:

China, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: Credential-bearing API calls can control camera privacy-mask state.

Mitigation: Review before installing and use only credentials and device tokens that are intended to grant camera privacy-mask control.

Risk: A nonstandard endpoint could receive credential-bearing requests.

Mitigation: Keep JF_ENDPOINT set to one of the documented JFTech hosts.

Risk: The toggle action does not determine the current mask state and can turn masking off.

Mitigation: Prefer explicit enable or disable commands until endpoint validation and toggle behavior are fixed.

## Reference(s):

- [JFTech Open Platform Documentation](https://docs.jftech.com)
- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-video-masking)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and textual command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JFTech account credentials, a device token, a device serial number, and a supported online PTZ device.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
