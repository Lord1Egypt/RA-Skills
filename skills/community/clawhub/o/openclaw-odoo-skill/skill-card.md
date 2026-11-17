## Description:

Build or use the Odoo ERP connector for OpenClaw (Sales, CRM, Purchase, Inventory, Projects, HR, Fleet, Manufacturing integration via XML-RPC).

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjrhjr](https://clawhub.ai/user/hjrhjr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to connect OpenClaw agents to authorized Odoo 19 environments and manage sales, CRM, purchasing, inventory, invoicing, projects, HR, fleet, manufacturing, calendar, and eCommerce workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live changes in Odoo business records, including orders, invoices, HR, inventory, manufacturing, deletion, and product publishing workflows.

Mitigation: Use a dedicated least-privilege Odoo API user, start in staging, and require human confirmation for high-impact or irreversible actions.

Risk: Odoo credentials and API tokens may be exposed if config files or environment files are mishandled.

Mitigation: Store secrets outside source control, protect and rotate API tokens, and avoid committing config.json or .env files.

Risk: Non-local Odoo connections over plain HTTP can expose credentials and business data.

Mitigation: Require HTTPS for any non-local Odoo server and verify network access controls before production use.

Risk: The optional webhook receiver can accept inbound requests and may be exposed publicly if deployed without controls.

Mitigation: Use a strong HMAC secret, TLS, request limits, and network allowlisting; do not expose the webhook publicly without those controls.

Risk: Smart auto-create behavior can create customers, products, projects, departments, employees, events, or other records from fuzzy matches.

Mitigation: Disable or restrict auto-create behavior where possible and review created-vs-found summaries before committing downstream actions.

Risk: Unpinned installer or Python dependency versions can change runtime behavior after installation.

Mitigation: Pin installer and Python dependency versions for production deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hjrhjr/skills/openclaw-odoo-skill)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [TEST_RESULTS.md](artifact/TEST_RESULTS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration examples, and JSON-style response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call configured Odoo XML-RPC APIs when installed with valid Odoo credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
