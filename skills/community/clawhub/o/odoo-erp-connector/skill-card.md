## Description:

Full-featured Odoo 19 ERP connector for OpenClaw - Sales, CRM, Purchase, Inventory, Projects, HR, Fleet, Manufacturing (80+ operations, complete Python code included, XML-RPC integration).

This skill is ready for commercial/non-commercial use.

## Publisher:

[nullnaveen](https://clawhub.ai/user/nullnaveen)

### License/Terms of Use:

MIT

## Use Case:

Developers and Odoo administrators use this skill to connect OpenClaw agents to Odoo 19 ERP workflows for sales, CRM, purchasing, inventory, invoicing, projects, HR, fleet, manufacturing, calendar, and ecommerce operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connector can create, update, delete, post, approve, receive, and complete important Odoo business records.

Mitigation: Review in a sandbox first, use a dedicated least-privilege Odoo API user, and require explicit human confirmation for destructive or financially material actions.

Risk: Credentials and connection settings are loaded from environment variables or config.json, and examples include non-local Odoo URLs.

Mitigation: Store API keys in protected secret storage, avoid committing config.json, and require HTTPS for every non-local Odoo endpoint.

Risk: The optional webhook server can bind broadly and signature checks depend on a configured HMAC secret.

Mitigation: Disable the webhook unless needed; when enabled, bind it to localhost or a protected network, require a strong HMAC secret, and place body-size and rate limits in front of it.

Risk: The installation example uses an unversioned npx command.

Mitigation: Prefer a pinned, verified installer or reviewed artifact before installing into an OpenClaw environment.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)
- [ClawHub package page](https://clawhub.ai/nullnaveen/skills/odoo-erp-connector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples and Python/configuration snippets; runtime calls return structured dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes natural-language ERP command examples and configuration values for Odoo XML-RPC access.]

## Skill Version(s):

1.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
