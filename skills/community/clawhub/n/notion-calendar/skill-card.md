## Description: <br>
Manage Notion calendar databases with date-aware search, page creation, rescheduling, and safe workflows for planning views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to operate Notion databases as calendars, editorial plans, launch schedules, content calendars, or dated task boards. It helps discover schemas, query bounded time windows, create pages, reschedule items, and verify updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may access Notion page titles, properties, dates, statuses, and content from databases shared with the integration. <br>
Mitigation: Scope the Notion integration to specific databases and use read-only or write-with-confirmation mode unless automated updates are intentional. <br>
Risk: Local memory may preserve workspace context, property mappings, defaults, and inferred routine patterns. <br>
Mitigation: Avoid saving sensitive routine details in ~/notion-calendar/ and review local memory files when defaults or mappings change. <br>
Risk: Ambiguous titles, duplicate calendar rows, or unverified schemas can cause incorrect updates. <br>
Mitigation: Resolve data source IDs and property names before writes, require explicit confirmation for destructive changes, and read back changed pages after updates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ivangdavila/notion-calendar) <br>
- [Skill homepage](https://clawic.com/skills/notion-calendar) <br>
- [Notion API search endpoint](https://api.notion.com/v1/search) <br>
- [Notion API database endpoint](https://api.notion.com/v1/databases/*) <br>
- [Notion API data source endpoint](https://api.notion.com/v1/data_sources/*) <br>
- [Notion API page endpoint](https://api.notion.com/v1/pages/*) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Notion API requests, local memory updates under ~/notion-calendar/, and read-back verification summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
