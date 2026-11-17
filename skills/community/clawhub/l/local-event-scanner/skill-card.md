## Description:

Finds and ranks local events for a user's location, dates, and interests, with source links and practical caveats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobiaswestholm](https://clawhub.ai/user/tobiaswestholm)

### License/Terms of Use:

MIT-0

## Use Case:

People looking for local events use this skill to discover and shortlist upcoming gatherings that fit their interests and availability. On explicit request, it can add a selected event to Google Calendar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar access may expose private availability beyond what is needed to find events.

Mitigation: Enable the connector only with the user's consent; limit lookups to busy/free information for the requested window and avoid storing private event details.

Risk: Optional weekly scans may run unexpectedly after setup.

Mitigation: Set up recurring scans only after the user agrees to their schedule and understands how to review or disable them.

Risk: Adding an event writes to the user's calendar.

Mitigation: Create only the specifically requested event after confirming its details; do not invite attendees or create a recurring event by default.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/tobiaswestholm/skills/local-event-scanner)
- [Operating Model](references/operating-model.md)
- [Privacy And Access](references/privacy-and-access.md)
- [Availability Rules](references/availability-rules.md)
- [Scoring Rubric](references/scoring-rubric.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown ranked shortlist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Event dates, venues, source links, price or booking details, fit, caveats, and confidence; optional calendar availability notes.]

## Skill Version(s):

1.1.5 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
