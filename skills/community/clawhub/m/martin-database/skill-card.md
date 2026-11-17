## Description:

Connect to Supabase for database operations including SQL queries, inserts, updates, deletes, vector similarity search, and table management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to inspect and modify Supabase data, run SQL and RPC workflows, and prepare vector search against pgvector-backed tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate with a Supabase service-role key that may bypass row-level security and allow broad data access or changes.

Mitigation: Use a non-production project or least-privilege key where possible, keep credentials out of shared logs, and verify SUPABASE_URL before running commands.

Risk: Raw SQL, RPC, update, upsert, and delete commands can alter or remove production data.

Mitigation: Manually review destructive or broad write commands before execution and test them against non-production data first.

Risk: Vector-search query text is sent to an external embedding service.

Mitigation: Avoid sensitive text in vector-search queries and confirm that the embedding service is acceptable for the data being processed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/martin-database)
- [Complete setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Supabase credentials for database operations and a SkillBoss API key for vector-search embeddings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
