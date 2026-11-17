## Description:

Ingest pasted PC parts purchase/config text into Notion DIY_PC tables, classify and enrich item details, ask follow-up questions for ambiguous records, and upsert rows through the Notion data_sources API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators who maintain DIY PC inventory in Notion use this skill to turn pasted purchase logs, receipts, and component notes into classified records for PCConfig, storage, enclosure, and PCInput tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live writes to Notion pages and databases.

Mitigation: Inspect generated JSONL before execution and use a Notion integration shared only with the intended DIY-PC databases.

Risk: Direct page updates, archive, and overwrite controls can modify or remove existing Notion content.

Mitigation: Avoid page_id, id, archive, and overwrite controls unless intentionally targeting a specific page change.

Risk: Notion tokens and database IDs are sensitive operational configuration.

Mitigation: Keep tokens in environment variables or local config files and do not publish real IDs or credentials.

## Reference(s):

- [Skill release page](https://clawhub.ai/nextaltair/skills/openclaw-skill-diy-pc-ingest)
- [ClawHub Notion dependency](https://clawhub.ai/steipete/notion)
- [Config example](references/config.example.json)
- [Notion ID setup notes](references/notion-ids.md)
- [Notion API endpoint](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSONL records and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform live Notion create, update, archive, or overwrite operations when run with valid credentials.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
