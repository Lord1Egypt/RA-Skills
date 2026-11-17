## Description:

Track grocery purchases and monitor food freshness using Supabase for grocery-order monitoring, expiry checks, pantry logging, morning summaries, and food-waste management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madebydia](https://clawhub.ai/user/madebydia)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and household agents use this skill to log grocery purchases, estimate shelf life, check expiring items, and update pantry item status from manual input or parsed grocery-order data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Grocery emails, order IDs, and pantry records can contain personal data.

Mitigation: Use authenticated user tokens, confirm consent before recurring email ingestion, and avoid storing more grocery or order detail than needed.

Risk: Pantry data stored in Supabase can be exposed if access controls are weak.

Mitigation: Use explicit per-user row-level security, restricted grants, and the anon key rather than a service-role key.

Risk: Commands such as bulk-add, refresh, use, and toss can mutate pantry records automatically.

Mitigation: Prefer dry-run or user confirmation behavior before running commands that add or update pantry records.

## Reference(s):

- [Default Shelf Life](artifact/references/shelf-life.md)
- [Supabase Schema](artifact/references/supabase-schema.sql)
- [Pantry Tracker ClawHub Listing](https://clawhub.ai/madebydia/skills/pantry-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples; CLI output is plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SUPABASE_URL and SUPABASE_KEY; some commands create or update pantry records.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
