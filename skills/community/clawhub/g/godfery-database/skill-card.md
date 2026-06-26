## Description: <br>
Connect to Supabase for database operations, vector search, and storage, including SQL queries, CRUD operations, pgvector similarity search, and table management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to administer Supabase-backed applications, inspect schemas, run SQL and REST-style table operations, call RPC functions, and perform vector similarity search with pgvector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete Supabase data and run raw SQL or RPC operations when supplied privileged credentials. <br>
Mitigation: Use a test project or least-privilege credentials where possible, avoid production service-role keys, and review each SQL, update, delete, upsert, and RPC action before execution. <br>
Risk: Vector-search text is sent to a third-party embedding provider through the SkillBoss API Hub. <br>
Mitigation: Do not submit sensitive vector-search text unless the embedding provider is trusted for that data. <br>
Risk: Supabase service-role keys can bypass Row Level Security and give the agent broad database access. <br>
Mitigation: Prefer scoped or restricted credentials for routine operations and reserve service-role keys for reviewed administrative tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/godfery-database) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with bash and SQL command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Supabase credentials and a SkillBoss API key for vector embedding generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
