## Description:

Connects agents to Supabase for database operations, vector search, storage-related workflows, SQL queries, pgvector similarity search, and table management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to let an agent run Supabase queries, CRUD operations, table inspection, RPC calls, and pgvector similarity search from documented shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Supabase service-role key, which can bypass Row Level Security and enable admin-level database access.

Mitigation: Use least-privilege or non-production credentials where possible, keep credentials out of logs and shared prompts, and verify SUPABASE_URL before running commands.

Risk: Raw SQL, update, delete, upsert, and RPC commands can modify or remove data broadly if used with unsafe inputs or filters.

Mitigation: Manually review each mutating command and prefer narrow filters, backups, and staging environments before production use.

Risk: Vector-search queries are sent to the embedding provider through SkillBoss API Hub.

Mitigation: Avoid sending sensitive query text for embedding unless the data-sharing path is approved for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/godfery-database)
- [ClawHub publisher profile](https://clawhub.ai/user/tobeyrebecca)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may call Supabase REST or RPC endpoints and return JSON-formatted API responses.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
