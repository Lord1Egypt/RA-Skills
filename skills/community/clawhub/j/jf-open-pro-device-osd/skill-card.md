## Description: <br>
Configures OSD watermark, channel title, time title, and privacy overlay settings for supported JF devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and device administrators use this skill to query and change JF camera OSD settings, including displayed channel names, timestamps, and privacy masks. <br>

### Deployment Geography for Use: <br>
Global, with documented JF regional API hosts for China, Asia, Europe, and North America. <br>

## Known Risks and Mitigations: <br>
Risk: The scripts can modify camera OSD settings, including channel titles and privacy overlays. <br>
Mitigation: Manually confirm the target device, channel, requested action, and current configuration before running any set operation. <br>
Risk: The skill uses sensitive JF credentials and a device token to sign API requests. <br>
Mitigation: Store the JF app secret and device token securely, avoid logging them, and rotate them if exposure is suspected. <br>
Risk: JF_ENDPOINT is configurable, so signed requests could be sent to an unintended host. <br>
Mitigation: Keep JF_ENDPOINT set only to an official JF regional API host before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-device-osd) <br>
- [JFTech publisher profile](https://clawhub.ai/user/jftech) <br>
- [JFTech documentation](https://docs.jftech.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with environment variables, shell commands, and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce signed HTTPS API requests when the bundled scripts are run with JF credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
