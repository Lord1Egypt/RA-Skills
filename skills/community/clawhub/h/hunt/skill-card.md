## Description:

Hunt turns an agent into a hackathon scout that finds online hackathons, vets them, tracks selected events in map.md, and sets reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lloyd-c137](https://clawhub.ai/user/lloyd-c137)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover free online hackathons, compare upcoming options, save selected events to a local tracker, and receive reminders before events start.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent browses public hackathon sites and may surface stale, incomplete, or changed event details.

Mitigation: Verify event pages for online status, cost, registration status, dates, and prize details before recommending or tracking an event.

Risk: The skill can read local user preferences, update the local map.md tracker, and create reminder jobs.

Mitigation: Use explicit add, remove, clear, and reminder commands; review tracked entries and scheduled reminders periodically.

Risk: The prize-only mode depends on event-page prize language that may be unclear.

Mitigation: Label unclear prize information as unknown and require confirmation before treating it as a cash-prize opportunity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lloyd-c137/skills/hunt)
- [Repository Metadata](https://github.com/lloyd-c137/hunt-skill)
- [Map Format Reference](artifact/references/map-format.md)
- [MLH Events](https://events.mlh.io/)
- [Devpost Hackathons](https://devpost.com/hackathons)
- [Devfolio Hackathons](https://devfolio.co/hackathons)
- [lablab.ai Hackathons](https://lablab.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Telegram-friendly Markdown or plain text, map.md entries, and reminder job configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local map.md tracker and propose reminder jobs when the user explicitly asks to track events.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
