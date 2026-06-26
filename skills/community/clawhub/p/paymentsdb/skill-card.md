## Description: <br>
Query Stripe customer and billing data from a synced PostgreSQL database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ramonverse](https://clawhub.ai/user/ramonverse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External operators and developers use this skill to answer questions about Stripe customers, subscriptions, invoices, charges, and related billing records from a read-only PostgreSQL replica. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent SQL access to sensitive Stripe billing data through a database replica. <br>
Mitigation: Use a dedicated read-only PostgreSQL role limited to the stripe schema and review query results for customer or financial data before sharing them. <br>
Risk: The setup flow asks the user to place database credentials in query.sh. <br>
Mitigation: Avoid committing or sharing query.sh after adding credentials, and rotate any password that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ramonverse/paymentsdb) <br>
- [Publisher profile](https://clawhub.ai/user/ramonverse) <br>
- [PaymentsDB provisioning site](https://paymentsdb.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline SQL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires psql and configured PostgreSQL credentials in query.sh.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
