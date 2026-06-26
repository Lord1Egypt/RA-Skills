## Description: <br>
Send and receive SMS messages through a self-hosted SMS Gateway running on a USB GSM modem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattboston](https://clawhub.ai/user/mattboston) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent send allowlisted SMS messages and check received SMS messages through a local, self-hosted GSM modem gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real SMS messages through the configured gateway. <br>
Mitigation: Confirm the recipient and message text before sending, and keep the allowlist limited to approved contacts. <br>
Risk: Checking unread messages marks displayed messages as read. <br>
Mitigation: Run receive commands only when it is acceptable to change unread message state, and communicate that side effect to users. <br>
Risk: The gateway API key grants access to SMS operations. <br>
Mitigation: Store SMS_GATEWAY_API_KEY with restrictive permissions or in a secret manager, and do not expose it in agent responses. <br>
Risk: The upstream installer configures a self-hosted service on the user's machine or device. <br>
Mitigation: Review the upstream installer and trust the self-hosted SMS Gateway service before installing or upgrading. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mattboston/gsm-sms-gateway) <br>
- [SMS Gateway README](https://github.com/mattboston/sms-gateway/blob/main/openclaw/README.md) <br>
- [SMS Gateway Repository](https://github.com/mattboston/sms-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON/text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, SMS_GATEWAY_API_KEY, and a configured allowlist. Receiving unread messages marks displayed messages as read.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
