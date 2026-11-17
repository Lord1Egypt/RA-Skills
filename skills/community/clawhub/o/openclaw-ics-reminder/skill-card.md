## Description:

Creates, lists, cancels, and rotates ICS-backed reminders through a configured reminder worker API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cute-angel](https://clawhub.ai/user/cute-angel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn reminder requests into calendar-backed reminder operations, including creating, listing, deleting, and rotating reminder feed access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured reminder API base URL can receive the reminder API token and reminder details.

Mitigation: Review REMINDER_API_BASE_URL before use, prefer a trusted HTTPS reminder worker, and reserve HTTP endpoints for loopback development such as 127.0.0.1.

Risk: Delete and feed-token rotation operations change remote reminder state or calendar feed access.

Mitigation: Confirm the exact reminder or feed-token rotation action with the user before running those operations.

Risk: Ambiguous dates, times, timezones, recurrence, or past reminders can create reminders at unintended times.

Mitigation: Ask a concise follow-up when scheduling details are missing or ambiguous and confirm normalized schedule details in the final response.

## Reference(s):

- [API Contract](references/api-contract.md)
- [OpenClaw Config](references/openclaw-config.md)
- [Time Parsing Rules](references/time-parsing-rules.md)
- [Calendar reminder ClawHub listing](https://clawhub.ai/cute-angel/skills/openclaw-ics-reminder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a Node.js helper that sends reminder API requests and prints JSON responses.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
