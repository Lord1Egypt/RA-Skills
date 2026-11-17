## Description:

Parses .ics / iCalendar files or URLs, expands recurring events (RRULE), filters by date range or keywords, and returns a clean JSON list of events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baptiste00001](https://clawhub.ai/user/baptiste00001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when an agent needs to parse local or remote iCalendar feeds, expand recurring events, and filter results by date range or keywords for scheduling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to arbitrary calendar URLs.

Mitigation: Install only when trusted calendar sources are expected; prefer local .ics files or known public calendar providers and avoid private or internal URLs.

Risk: The local-file boundary may be weak when workspace symlinks point outside allowed paths.

Mitigation: Review workspace symlinks and avoid placing sensitive files under allowed paths until the file-boundary behavior is tightened.

Risk: Large calendars or broad recurrence expansion can create resource pressure.

Mitigation: Use bounded date ranges and conservative recurrence limits when asking the agent to process calendar feeds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baptiste00001/skills/icalendar-events-parser)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON object with success status, event count, event records, and error details when parsing fails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Events include UID, title, start, end, all-day flag, description, location, recurrence ID, and original RRULE fields when available.]

## Skill Version(s):

1.0.2 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
