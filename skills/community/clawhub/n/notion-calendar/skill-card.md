## Description:

Manage Notion calendar databases with date-aware search, page creation, rescheduling, and safe workflows for planning views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to work with Notion databases as calendars for editorial plans, launch schedules, content calendars, and dated task boards. It helps discover calendar schemas, query bounded time windows, create pages, reschedule items, and verify writes through Notion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar titles, dates, page properties, and related planning content may be sent to Notion through the official API.

Mitigation: Use a scoped Notion integration, share only the intended databases with that integration, and avoid using the skill for workspaces where that data should not leave the local environment.

Risk: Incorrect writes could update the wrong calendar row when titles are duplicated or schema fields are ambiguous.

Mitigation: Verify database and data source IDs, confirm property mappings before writes, require explicit confirmation for destructive changes, and read back changed pages after updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/notion-calendar)
- [Skill homepage](https://clawic.com/skills/notion-calendar)
- [Setup](setup.md)
- [Calendar Database Schema](calendar-schema.md)
- [Calendar Source Mapping](calendars.md)
- [Query and Reschedule Playbook](query-playbook.md)
- [Optional CLI Patterns](cli-patterns.md)
- [Troubleshooting](troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Notion calendar memory files under ~/notion-calendar/ after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
