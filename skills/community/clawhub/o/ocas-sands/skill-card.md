## Description:

Sands helps agents view, create, modify, delete, and analyze calendar events, including scheduling conflicts, free slots, travel-time blocks, recurring events, and daily schedule briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use Sands to manage Google Calendar workflows through natural language, including event changes, conflict checks, availability searches, travel-time insertion, and structured schedule briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled calendar automation with OAuth-backed access can act on sensitive personal or work calendars.

Mitigation: Install only when that access is intended, review configured calendars and credentials before use, and keep calendar mutation commands under explicit user control.

Risk: Silent scheduled self-updates can change skill behavior without a deliberate review.

Mitigation: Disable or remove the daily self-update, avoid git reset or clean update paths, and require explicit approval before applying updates.

Risk: Chronicle sync can persist sensitive calendar facts such as medical, travel, and personal events into another datastore.

Mitigation: Make Chronicle sync opt-in and use category controls for medical, travel, and personal event classes.

Risk: Local journals and logs may retain calendar details beyond the immediate interaction.

Mitigation: Review retention settings, log locations, and journal contents before deployment in shared or regulated environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/indigokarasu/skills/ocas-sands)
- [Calendar configuration](references/calendar_config.md)
- [Credential files](references/credential-files.md)
- [Conflict detection](references/conflict_detection.md)
- [Conflict report format](references/conflict-report-format.md)
- [Direct calendar access](references/direct_calendar_access.md)
- [Chronicle sync](references/chronicle_sync.md)
- [Self-update behavior](references/self-update-sands.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSONL records, calendar API actions, and Python or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify calendar events, register scheduled jobs, write local journals and logs, and sync selected calendar facts when invoked with appropriate tools and credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; source skill metadata.version is 2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
