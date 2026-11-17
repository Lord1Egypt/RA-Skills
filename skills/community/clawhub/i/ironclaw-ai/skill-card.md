## Description:

IronClaw AI is a military-style productivity operating system for mission, habit, goal, tennis, sleep, discipline-score, briefing, and coaching requests in English or Indonesian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[susiloandreas](https://clawhub.ai/user/susiloandreas)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route natural-language productivity, sleep, tennis, goal, and coaching requests into structured IronClaw service commands and display the service response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send personal productivity, habit, tennis, sleep, and coaching inputs to a configurable external service where they may be stored remotely.

Mitigation: Use only with a trusted IRONCLAW_SERVICE_URL, clear data-retention expectations, and explicit acceptance before entering personal data.

Risk: Scheduled automations can poll external notification endpoints and deliver recurring coaching messages.

Mitigation: Disable scheduled automations or make them opt-in unless recurring external polling and unsolicited coaching messages are intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text responses derived from JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IRONCLAW_SERVICE_URL; commands may send personal productivity, habit, tennis, sleep, and coaching data to the configured service.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
