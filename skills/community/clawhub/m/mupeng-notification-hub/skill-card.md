## Description: <br>
Unified notification hub collecting all skill alerts and delivering by priority <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to centralize local skill event notifications, prioritize urgent, important, and informational alerts, and route summaries to Discord, heartbeat responses, or daily reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local event files may include sensitive notification content that can appear in summaries, Discord alerts, or retained history. <br>
Mitigation: Avoid placing sensitive message bodies in events unless the destination channels and retention behavior are acceptable. <br>
Risk: Unclear event writer permissions or notification destinations can cause unexpected alerts or disclosure. <br>
Mitigation: Confirm which skills can write to events/, what notification content is allowed, and where Discord messages are sent before installation. <br>
Risk: Notification history can retain operational details longer than intended. <br>
Mitigation: Set an appropriate retention policy for memory/notifications/ before using the skill with real event data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/mupeng-notification-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured notification summaries, JSON examples, and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local event files, notification history, Discord delivery, and priority routing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
