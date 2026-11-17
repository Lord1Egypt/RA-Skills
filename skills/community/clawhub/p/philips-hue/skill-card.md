## Description:

Local control of Philips Hue lights via API v1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aprilox](https://clawhub.ai/user/aprilox)

### License/Terms of Use:


## Use Case:

Developers and home automation users use this skill to configure and run shell commands that control Philips Hue lights on a local network, including power, brightness, named colors, hex colors, hue, saturation, and color temperature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports input-handling flaws that can allow local code execution in normal use paths.

Mitigation: Review before installing, use only trusted color values, and prefer a version that validates hex colors and passes values to Python as data.

Risk: The security guidance reports that the .env file is sourced by the shell script.

Mitigation: Keep the skill directory and .env file writable only by the local user, and prefer a version that parses .env without executing it.

Risk: The security guidance reports that the Hue API username may be exposed to devices able to observe the local network.

Mitigation: Use the skill only on trusted local networks and document the HTTP credential exposure before deployment.

## Reference(s):

- [Philips Hue Developer Documentation](https://developers.meethue.com/)
- [ClawHub Philips Hue Skill](https://clawhub.ai/aprilox/skills/philips-hue)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, python3, a local Philips Hue Bridge, and a configured .env file containing BRIDGE_IP and USERNAME.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
