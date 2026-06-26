## Description: <br>
Notify guides agents in choosing notification channels, timing, formatting, escalation, and logging so user alerts are useful without creating notification fatigue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Notify to configure user-facing notifications, including channel choice, quiet hours, batching, escalation limits, and message format. It is intended for notification guidance and configuration rather than direct message delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notifications may be sent through inappropriate channels, outside the user's timezone or quiet hours, or too frequently. <br>
Mitigation: Set explicit channels, timezone, quiet hours, batching rules, escalation limits, and log retention before use. <br>
Risk: Escalation can become intrusive if reminders continue indefinitely or contact people without permission. <br>
Mitigation: Limit reminders, use secondary channels only when configured, stop after the defined escalation limit, and never contact others without explicit permission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/notify) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with examples, routing tables, checklists, and notification templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown-only skill; no hidden code, credential handling, or behavior outside notification guidance is indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, released 2026-02-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
