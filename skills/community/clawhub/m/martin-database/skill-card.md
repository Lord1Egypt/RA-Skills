## Description: <br>
Connects an agent to Supabase for SQL queries, CRUD operations, table inspection, RPC calls, and pgvector similarity search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and administer Supabase-backed databases, run SQL and REST operations, and perform vector similarity search over pgvector tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Supabase service-role credentials that can bypass row-level security and modify production data. <br>
Mitigation: Use least-privilege or non-production credentials when possible, keep credentials out of prompts and logs, and approve write, delete, raw SQL, and RPC actions before execution. <br>
Risk: Vector-search query text is sent to an external embedding endpoint. <br>
Mitigation: Avoid vector-search queries containing secrets, personal data, customer data, or proprietary text unless that external processing is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godferylindsay/martin-database) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and SQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Supabase credentials and uses an external embedding API for vector-search queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
