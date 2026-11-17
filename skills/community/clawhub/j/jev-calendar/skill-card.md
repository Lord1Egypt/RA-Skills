## Description:

Use Jev and WorkerKit to classify Google Calendar and Outlook events for AI-powered schedule analysis, meeting prioritization, and calendar triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workerkit](https://clawhub.ai/user/workerkit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and calendar operators use this skill to install, configure, deploy, and run a WorkerKit decision worker that classifies bounded Google Calendar or Outlook event samples into user-approved categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires scoped access to calendar event details and WorkerKit deployment/run permissions.

Mitigation: Review OAuth scopes, connected calendar identity, budget ceilings, and sample window before approving setup or runs.

Risk: Calendar event fields may include sensitive meeting titles, descriptions, locations, organizer names, and attendee details.

Mitigation: Use bounded samples, keep source text as evidence only, avoid pasting OTPs or provider secrets into chat, and report coverage limits clearly.

Risk: A capped event search can be mistaken for complete calendar coverage or an accuracy guarantee.

Mitigation: Report actual window, item caps, judged and omitted counts, unclear cases, and unknown completeness when continuation data is unavailable.

## Reference(s):

- [Calendar Jev Classifier kit](https://workerkit.ai/kit/calendar-jev-classifier)
- [OpenClaw setup](https://docs.openclaw.ai/start/getting-started)
- [WorkerKit OpenClaw connection guide](https://workerkit.ai/openclaw/setup.md)
- [WorkerKit fleet skill](https://workerkit.ai/openclaw/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/workerkit/skills/jev-calendar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports worker and run links, counts, coverage limits, warnings, omissions, and cost information when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
