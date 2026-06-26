## Description: <br>
Manages JFTech device smart alarm capabilities, alarm switches, notification settings, schedules, alarm lists, and alarm image retrieval after the required device and OpenAPI credentials are configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query JFTech alarm-capable devices, adjust motion detection and notification behavior, configure alarm schedules, and retrieve alarm records or image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can disable alarms, change notification behavior, or alter schedules on live devices. <br>
Mitigation: Require explicit human confirmation before running actions that change alarm switches, notification settings, or time sections. <br>
Risk: The skill handles JFTech credentials, device identifiers, tokens, and alarm image URLs. <br>
Mitigation: Keep JF_* values out of shared shells and logs, use only documented endpoint values, and avoid exposing retrieved alarm images or URLs beyond authorized users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-device-smart-alarm) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jftech) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-oriented alarm data descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command-line instructions for a Python script that calls JFTech OpenAPI endpoints using environment-provided credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
