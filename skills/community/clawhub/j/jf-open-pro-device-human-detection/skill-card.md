## Description: <br>
Controls JFTech device human detection and PTZ human tracking settings through JFTech OpenAPI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and device administrators use this skill to inspect and change human detection, sensitivity, PTZ tracking, tracking sensitivity, and return-time settings on authorized JFTech camera devices. <br>

### Deployment Geography for Use: <br>
China Mainland (CN), Asia (AS), Europe (EU), and North America (NA) <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live camera human-detection and tracking behavior. <br>
Mitigation: Use it only with JFTech devices you own or are authorized to administer, and check current settings before running any set action. <br>
Risk: The skill sends signed device-management requests to an environment-selected host. <br>
Mitigation: Set JF_ENDPOINT only to an official JFTech regional host. <br>
Risk: JF_APP_SECRET and JF_DEVICE_TOKEN authorize device-management operations. <br>
Mitigation: Protect and rotate JF_APP_SECRET and JF_DEVICE_TOKEN. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jftech/jf-open-pro-device-human-detection) <br>
- [JFTech Open Platform documentation](https://docs.jftech.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown documentation and Python command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JFTech OpenAPI credentials, a device token, an authorized device serial number, and the selected regional endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
