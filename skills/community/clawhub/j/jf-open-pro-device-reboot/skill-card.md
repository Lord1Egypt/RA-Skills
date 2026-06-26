## Description: <br>
Supports authenticated remote reboot requests for JFTech devices, with shutdown requests available for some devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators managing JFTech-connected devices use this skill to configure credentials and run reboot or shutdown requests against bound, online devices. <br>

### Deployment Geography for Use: <br>
China Mainland, Asia, Europe, and North America <br>

## Known Risks and Mitigations: <br>
Risk: Remote reboot or shutdown can interrupt service for the targeted device. <br>
Mitigation: Require explicit operator confirmation of the device and action before execution, and schedule operations when temporary device downtime is acceptable. <br>
Risk: JFTech app secrets and device tokens are required to authorize the operation. <br>
Mitigation: Store credentials outside prompts and logs, restrict access to the runtime environment, and rotate tokens or secrets if exposure is suspected. <br>
Risk: A misconfigured JF_ENDPOINT can send signed requests to the wrong API host. <br>
Mitigation: Pin JF_ENDPOINT to the intended official regional JFTech API host before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-device-reboot) <br>
- [JFTech Open Platform documentation](https://docs.jftech.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JFTech credentials, a device token, a bound device, and an online device before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
