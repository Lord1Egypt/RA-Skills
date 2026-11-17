## Description:

Query Stripe customer and billing data from a synced PostgreSQL database. Use when the user asks about Stripe customers, subscriptions, invoices, charges, or any Stripe-related data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramonverse](https://clawhub.ai/user/ramonverse)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to answer questions about Stripe customers, subscriptions, invoices, charges, and related billing records by querying a synced PostgreSQL database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent receives SQL access to a synced Stripe billing database.

Mitigation: Use a dedicated read-only PostgreSQL role restricted to the needed Stripe views, and review queries before execution.

Risk: The setup flow encourages credentials to be placed directly in query.sh.

Mitigation: Store credentials outside the script when possible and rotate any credentials that were stored or shared this way.

Risk: The SQL wrapper does not prevent non-Stripe or mutating SQL.

Mitigation: Restrict database privileges to read-only access and only install the skill when broad SQL query access is acceptable.

## Reference(s):

- [PaymentsDB](https://paymentsdb.com)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Markdown with inline shell and SQL snippets; psql output is unaligned text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires psql and a configured read-only PostgreSQL connection; SQL is passed as a single quoted argument.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
