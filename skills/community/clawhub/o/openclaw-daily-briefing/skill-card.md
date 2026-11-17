## Description:

OpenClaw Daily Briefing generates a concise morning brief that combines weather, calendar, to-do, news, and commute information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangkai258](https://clawhub.ai/user/yangkai258)

### License/Terms of Use:

MIT-0

## Use Case:

Users can request or schedule a Chinese-language weekday morning briefing to review weather, meetings, tasks, news, and commute considerations before starting the workday.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar, to-do, news, and scheduled briefing integrations may expose sensitive meetings, tasks, or account data in generated output.

Mitigation: Confirm which accounts are connected and limit displayed briefing content to information appropriate for the deployment context.

Risk: The weather helper retrieves and displays external weather responses, and the evidence recommends transport-security and sanitization improvements.

Mitigation: Use HTTPS for weather requests and sanitize displayed responses before relying on scheduled or repeated briefings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangkai258/skills/openclaw-daily-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style briefing text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; optional calendar, to-do, news, and scheduled briefing integrations may require connected accounts or APIs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
