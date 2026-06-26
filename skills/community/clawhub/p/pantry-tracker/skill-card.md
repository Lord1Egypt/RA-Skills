## Description: <br>
Track grocery purchases and monitor food freshness using Supabase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meimakes](https://clawhub.ai/user/meimakes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to log pantry items from grocery orders, estimate freshness windows, query expiring food, and generate morning pantry summaries through a Supabase-backed CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores email-derived grocery data, including optional order references, in Supabase. <br>
Mitigation: Use a private Supabase project, avoid storing order IDs unless needed, and review what grocery-order content is parsed before enabling recurring scans. <br>
Risk: The included database setup lacks the access controls implied by anon-key usage. <br>
Mitigation: Add Row Level Security policies before using an anon key and never use a service role key for pantry operations. <br>


## Reference(s): <br>
- [Pantry Tracker on ClawHub](https://clawhub.ai/meimakes/pantry-tracker) <br>
- [Default Shelf Life](references/shelf-life.md) <br>
- [Supabase Schema](references/supabase-schema.sql) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and plain-text CLI summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUPABASE_URL and SUPABASE_KEY; the skill expects the agent to use a separate email tool for grocery-order scanning.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
