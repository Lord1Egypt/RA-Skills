## Description:

Track hackathon deadlines, prizes, submission checklists, calendar milestones, and progress, including extracting hackathon details from URLs to populate entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonbistudio](https://clawhub.ai/user/tonbistudio)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to maintain hackathon records, monitor upcoming deadlines, manage submission checklists, and sync milestones to Google Calendar through the gog CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google Calendar removal can delete unrelated events when a short or broad hackathon name matches event titles.

Mitigation: Review matching events with gcal list first, avoid short or empty names, and prefer a dedicated calendar or manual deletion until removal is limited to stored event IDs or exact skill-owned titles.

Risk: Calendar sync uses an authenticated gog CLI to access Google Calendar.

Mitigation: Install and authenticate gog only in accounts where calendar access is acceptable, and review created [REG], [WORK], and [DEADLINE] events.

Risk: The skill stores hackathon data locally under ~/.openclaw/workspace/hackathons.json.

Mitigation: Avoid storing sensitive project details in tracked hackathon names, prizes, or checklist items.

Risk: URL-based setup depends on fetching user-provided hackathon pages and extracting event data accurately.

Mitigation: Verify extracted deadlines, prizes, and requirements against the source page before adding or syncing events.

## Reference(s):

- [Hackathon Manager ClawHub listing](https://clawhub.ai/tonbistudio/skills/hackathon-manager)
- [gog CLI](https://github.com/rubiojr/gog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-backed local state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores hackathon data locally at ~/.openclaw/workspace/hackathons.json and can call the authenticated gog CLI for Google Calendar operations.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
