## Description: <br>
Trigger and manage OpenClaw outbound phone receipts via ElevenLabs+Twilio for task completion/failure notifications. Use when user asks to call them after finishing/failing a task, asks to enable/disable fixed command toggles ("phone-receipt=on/off"), asks to test call quality, or asks to persist phone receipt behavior across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuofangzhe](https://clawhub.ai/user/tuofangzhe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and automation developers use this skill to persist phone receipt preferences, trigger outbound completion or failure calls, and configure ElevenLabs plus Twilio callback notifications. It is intended for tasks where the user explicitly wants a phone receipt, urgent notification, failure notification, or call-quality test. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist notification automation and initiate outbound phone-call behavior. <br>
Mitigation: Confirm the recipient, task scope, and enabled policy before use, and use phone-receipt=off when notifications should stop. <br>
Risk: Telegram task summaries may disclose task details without enough setup, consent, or scoping detail. <br>
Mitigation: Review who receives Telegram summaries and what information may be included before enabling the skill. <br>
Risk: The ElevenLabs and Twilio setup depends on sensitive environment variables and a target phone number. <br>
Mitigation: Protect the .env.elevenlabs-call file, replace the sample phone number, and verify API key scope and Twilio caller requirements before triggering calls. <br>


## Reference(s): <br>
- [OpenClaw Phone Receipt on ClawHub](https://clawhub.ai/tuofangzhe/openclaw-phone-receipt) <br>
- [OpenClaw Phone Receipt Setup](references/setup.md) <br>
- [Sample ElevenLabs Call Environment](references/env-example.txt) <br>
- [ClawHub Upload Checklist](references/publish-clawhub.md) <br>
- [ElevenLabs Twilio Outbound Call API Endpoint](https://api.elevenlabs.io/v1/convai/twilio/outbound-call) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, environment configuration, and JSON state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write memory/phone-receipt-state.json and initiate outbound calls through ElevenLabs when enabled by policy.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
