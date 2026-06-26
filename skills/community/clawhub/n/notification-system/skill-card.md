## Description: <br>
Manage outbound notifications across WhatsApp, Telegram, and email with templates, scheduling, delivery tracking, and rate limiting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[engibarian](https://clawhub.ai/user/engibarian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to draft, queue, schedule, and track outbound notifications across WhatsApp, Telegram, and email for operational, appointment, payment, support, marketing, and alert workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward sending real outbound messages. <br>
Mitigation: Require explicit human approval for sends and scheduled jobs, and start with test recipients before enabling production targets. <br>
Risk: Delivery logs and queue entries can contain recipient contact details. <br>
Mitigation: Define retention, masking, and deletion rules before use, and restrict access to queue and delivery log files. <br>
Risk: Automatic fallback across channels can contact recipients through an unintended medium. <br>
Mitigation: Confirm opt-in status per recipient and per channel before enabling fallback from WhatsApp to Telegram or email. <br>
Risk: Marketing or broadcast templates can create spam, consent, or rate-limit problems. <br>
Mitigation: Use the configured rate limits, quiet hours, deduplication window, and opt-out handling before sending bulk messages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/engibarian/notification-system) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Rate limiter configuration](artifact/rate-limiters.json) <br>
- [Template index](artifact/templates/index.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown templates, JSON queue and rate-limit configuration, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes message templates for WhatsApp, Telegram, and email plus queue, scheduling, delivery tracking, rate limiting, quiet hours, retry, and deduplication guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
