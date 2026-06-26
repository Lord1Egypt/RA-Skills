## Description: <br>
Send and read SMS text messages via an Android phone using pidge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[typhonius](https://clawhub.ai/user/typhonius) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to send SMS, read an SMS inbox, check delivery status, and manage processed message state through pidge on an Android phone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send SMS through an Android phone, so mistaken recipients or message content could result in real outbound texts. <br>
Mitigation: Personally confirm the recipient and message content before any text is sent, and do not send bulk or repeated messages. <br>
Risk: The skill can read SMS inbox content, which may expose private or sensitive messages. <br>
Mitigation: Protect ~/.config/pidge/config.toml and avoid revealing full private SMS content unless directly requested in an appropriate private context. <br>
Risk: The skill depends on the upstream pidge CLI and the Android SMS Gateway configuration. <br>
Mitigation: Review the upstream pidge CLI before installing and verify the gateway configuration before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub pidgesms page](https://clawhub.ai/typhonius/pidgesms) <br>
- [pidge](https://github.com/typhonius/pidge) <br>
- [Android SMS Gateway](https://github.com/capcom6/android-sms-gateway) <br>
- [OpenClaw](https://openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference SMS recipients, delivery state, inbox entries, and pidge configuration details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
