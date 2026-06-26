## Description: <br>
One-shot reminders via natural language. Auto-detects channel and timezone. Say 'remind me...' in any language and get pinged when it's time. Works with every channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ethan-Shen-Individual-Lab](https://clawhub.ai/user/Ethan-Shen-Individual-Lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an OpenClaw agent for one-time reminders in natural language, then list, cancel, or configure reminder delivery across chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder text, timing, channel, timezone, and optional delivery target may be stored locally or in OpenClaw cron until delivery or cancellation. <br>
Mitigation: Avoid putting secrets in reminders and cancel reminders that should no longer be retained. <br>
Risk: Misconfigured channel, timezone, or delivery target can send a reminder to the wrong place or at the wrong time. <br>
Mitigation: Verify channel, target, and timezone settings in shared or multi-channel environments before relying on scheduled delivery. <br>


## Reference(s): <br>
- [Ping Me ClawHub Listing](https://clawhub.ai/Ethan-Shen-Individual-Lab/ping-me) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and concise natural-language confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates, lists, cancels, and configures one-time OpenClaw reminders; reminder text, timing, channel, timezone, and optional delivery target may be stored locally or in OpenClaw cron until delivery or cancellation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
