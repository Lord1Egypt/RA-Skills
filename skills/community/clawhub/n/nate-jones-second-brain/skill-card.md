## Description:

Set up and operate a personal knowledge system that uses Supabase with pgvector and OpenRouter to capture notes, classify them, route them into structured tables, and search them semantically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justfinethanku](https://clawhub.ai/user/justfinethanku)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure and operate a single-user second-brain workflow for capturing thoughts, tasks, relationships, projects, and ideas into a searchable Supabase database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Captured notes, names, tasks, and action items are sent to OpenRouter and stored in Supabase.

Mitigation: Use the skill only for data you are comfortable processing through those services, and avoid secrets, regulated data, or broadly sensitive personal and work records.

Risk: The workflow depends on a Supabase service-role key with broad database access.

Mitigation: Use a dedicated Supabase project, keep credentials in server-side or private agent configuration only, rotate keys periodically, and prefer a scoped backend or restricted database role before expanding use.

Risk: LLM classification can route information to the wrong table or create misleading structured records.

Mitigation: Review confirmation messages, leave low-confidence items in the inbox, and use correction workflows to move records and preserve the audit trail.

## Reference(s):

- [Conceptual Framework](artifact/references/concepts.md)
- [First-Time Setup](artifact/references/setup.md)
- [Database Schema](artifact/references/schema.md)
- [Ingest Pipeline](artifact/references/ingest.md)
- [Retrieval Operations](artifact/references/retrieval.md)
- [OpenRouter API Patterns](artifact/references/openrouter.md)
- [Nate Jones homepage](https://natebjones.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, SQL, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Supabase and OpenRouter credentials supplied by the user environment.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
