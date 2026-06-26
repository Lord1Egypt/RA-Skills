## Description: <br>
Period Care Assistant helps OpenClaw users privately log menstrual-cycle starts, check current cycle status, predict next start dates, and prepare reminder schedules using local encrypted storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjian124](https://clawhub.ai/user/wangjian124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and assistants use this skill to record menstrual-cycle start dates, answer cycle-status questions, estimate upcoming starts, and prepare reminders while keeping history local and encrypted. It supports personal tracking workflows and should not be treated as medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Menstrual-cycle history is sensitive health-related data stored locally under a secret key. <br>
Mitigation: Use a strong PERIOD_TRACKER_KEY, keep the encrypted store and configuration private, and avoid placing real user data or secrets in public ClawHub releases. <br>
Risk: Reminder delivery through chat or webhook routes can expose sensitive health information. <br>
Mitigation: Leave deliveryMode set to none unless reminders are intentionally enabled, and use webhook delivery only with endpoints the user controls and trusts. <br>
Risk: Cycle forecasts and phase labels are estimates and may be unreliable with sparse or irregular history. <br>
Mitigation: Describe predictions as data-based estimates, include uncertainty when confidence is low, and suggest professional medical advice for severe pain, unusual bleeding, or highly irregular cycles. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangjian124/period-care-assistant) <br>
- [OpenClaw ClawHub Documentation](https://docs.openclaw.ai/tools/clawhub) <br>
- [Deployment Notes](references/deployment.md) <br>
- [Forecast Model And Privacy](references/model-and-privacy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local encrypted storage keyed by PERIOD_TRACKER_KEY; reminder delivery depends on the configured OpenClaw channel or webhook.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
