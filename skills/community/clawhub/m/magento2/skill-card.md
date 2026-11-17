## Description:

Manage Magento 2 and Adobe Commerce stores through REST API workflows for orders, catalog, customers, inventory, promotions, sales reporting, diagnostics, and custom module endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caravanglory](https://clawhub.ai/user/caravanglory)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, store operators, and support teams use this skill to inspect and manage Magento 2 or Adobe Commerce stores from an agent workflow. It supports read-only reporting and diagnostics as well as confirmed write operations such as inventory, catalog, order, promotion, cache, and custom API changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Magento API credentials may grant access to customer, order, catalog, and store-management data.

Mitigation: Use least-privilege Magento integration tokens, store them only in environment variables, and avoid exposing credentials in chat, logs, or summaries.

Risk: The skill can perform high-impact store mutations such as order cancellation, product deletion, pricing updates, stock updates, promotion changes, cache clearing, and custom API writes.

Mitigation: Confirm every write command before execution, preview bulk operations first, and use staging or backups for changes with broad business impact.

Risk: Custom API POST, PUT, and DELETE calls can affect endpoints whose behavior depends on installed Magento modules.

Mitigation: Use custom API writes only for known endpoints, verify the request body and method, and prefer read-only schema discovery before mutation.

Risk: Reports and customer/order lookups can expose customer PII and commercially sensitive store data.

Mitigation: Treat generated reports as sensitive, limit sharing to authorized users, and redact customer details when they are not needed.

Risk: Transport and retry behavior should be reviewed before using the skill against production stores.

Mitigation: Configure only HTTPS Magento base URLs, review retry effects for write operations, and start with low-volume operations before bulk execution.

## Reference(s):

- [Magento 2 REST API Quick Reference](artifact/references/api-reference.md)
- [Magento 2 Diagnostics Reference](artifact/references/diagnostics.md)
- [AI Agent Workflow Reference](artifact/references/workflows.md)
- [Source homepage](https://github.com/caravanglory/openclaw-magento2)
- [ClawHub skill page](https://clawhub.ai/caravanglory/skills/magento2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, tables, JSON summaries, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Python helper scripts that print UTF-8 tables or JSON to stdout; write operations require explicit user confirmation.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
