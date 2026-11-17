## Description:

Find nearby OpenClaw meetups and related AI/agent community events, summarize the best matches, and help with reminder or share-ready text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawnewsde](https://clawhub.ai/user/clawnewsde)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find upcoming OpenClaw or AI/agent community events near a chosen location, compare a short ranked list, and draft reminder or share-ready text after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask for city or postal code information to find local events.

Mitigation: Provide only the minimum location detail needed for the search, and prefer city-level preferences when exact postal code precision is unnecessary.

Risk: Reminder, scheduling, saved preference, or sharing requests could create persistent or external effects.

Mitigation: Approve those actions only when intended; the skill is designed to require explicit confirmation before reminders, messages, persistence, or scheduling.

Risk: Event listings from web or event searches can be stale, duplicated, incomplete, or outside the requested scope.

Mitigation: Prefer future events with concrete date, location, and event-page evidence, and verify important details before attending or sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clawnewsde/skills/meetup)
- [Ranking and Selection](references/ranking.md)
- [Source Strategy](references/sources.md)
- [State and Reminders](references/state-and-reminders.md)
- [Meetup Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include event shortlists, ranking rationale, event links, reminder text, and share-ready drafts; persistent or external actions require explicit user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
