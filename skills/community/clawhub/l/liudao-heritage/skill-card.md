## Description:

Search, enrich, and manage family heritage and historical relationship data from the LiùDào (六道) SQLite database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirius-777-llm](https://clawhub.ai/user/sirius-777-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query historical figures, resolve family relationships, and manage LiùDào genealogy records with privacy controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read or modify private family records using weakly scoped viewer identity and local database code paths.

Mitigation: Run it only in trusted LiùDào workspaces, require authenticated viewer identity, and require explicit confirmation before database writes.

Risk: Database access depends on local liudao-bot modules and database operators outside the packaged artifact.

Mitigation: Review the local db_manager and relation_engine implementation before using the skill with personal data.

## Reference(s):

- [Liudao Heritage on ClawHub](https://clawhub.ai/sirius-777-llm/skills/liudao-heritage)
- [六道 Database Schema](references/db_schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database query results, relationship-resolution summaries, or record-management guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
