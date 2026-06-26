## Description: <br>
Send automated notifications to Dooray! messenger channels via webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iizs](https://clawhub.ai/user/iizs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams use this skill to send OpenClaw-requested status updates and notifications into configured Dooray chat rooms through incoming webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured Dooray webhook URLs act as credentials and can post to their associated rooms if exposed. <br>
Mitigation: Store webhook URLs only in the local OpenClaw config with restricted file permissions and rotate any webhook that may have been exposed. <br>
Risk: Disabling SSL verification can allow interception or spoofing on untrusted networks. <br>
Mitigation: Keep verify_ssl set to true unless the network and proxy setup is trusted and explicitly approved. <br>
Risk: Webhook messages may disclose sensitive operational or private information to chat rooms. <br>
Mitigation: Avoid sending passwords, secrets, regulated data, or private incident details unless that use is approved for the environment. <br>


## Reference(s): <br>
- [Dooray Incoming Webhook API Reference](references/dooray-api.md) <br>
- [Dooray Homepage](https://dooray.com) <br>
- [Dooray Helpdesk](https://helpdesk.dooray.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/iizs/openclaw-dooray-hook-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Plain text messages and JSON webhook payloads, with Markdown setup guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and configured Dooray webhook room URLs under skills.entries.dooray-hook.config; Dooray webhook messages are plain text.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
