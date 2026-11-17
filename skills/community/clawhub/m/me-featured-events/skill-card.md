## Description:

ME Event 精选 helps agents browse ME News AI and Web3 events, filter by region and date, and set up confirmed daily or near-real-time reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[me-news](https://clawhub.ai/user/me-news)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and agents use this skill to discover upcoming ME News AI and Web3 events and manage event reminder subscriptions with explicit delivery and schedule confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring reminders make repeated requests to api.me.news and can continue until paused or unsubscribed.

Mitigation: Confirm the delivery destination and schedule before creating reminders, and use the documented pause or unsubscribe flow when reminders are no longer wanted.

Risk: Delivery credentials could be exposed if channel tokens are stored in the skill directory or local state file.

Mitigation: Keep channel tokens outside the skill directory and state file, using the agent platform's secure delivery mechanism instead.

Risk: Incremental event delivery can repeat a notification if delivery succeeds but success feedback is not recorded.

Mitigation: Use a scheduler or delivery wrapper that records success only after confirmed delivery and leaves pending delivery unchanged on failure or unknown results.

## Reference(s):

- [ME Event Skill API](references/api.md)
- [Agent compatibility](references/agent-compatibility.md)
- [ME Featured Events Sources](sources.md)
- [ME Featured Events Output Format](format.md)
- [ME Event API base](https://api.me.news/skill/events)
- [ClawHub skill page](https://clawhub.ai/me-news/skills/me-featured-events)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style event reminder text with inline shell commands and JSON state examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses deterministic Node.js scripts; emits no message when there are no matching events.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
