## Description: <br>
Manage a Magento 2 or Adobe Commerce store through REST API workflows for orders, catalog, customers, inventory, promotions, sales reporting, store health diagnostics, and custom endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caravanglory](https://clawhub.ai/user/caravanglory) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and store administrators use this skill to inspect and manage Magento 2 or Adobe Commerce stores from an agent workflow, including reports, diagnostics, inventory updates, order actions, promotions, and custom REST endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make production store changes including order actions, product deletion, price and inventory updates, promotion changes, cache flushes, and custom API writes. <br>
Mitigation: Use a dedicated least-privilege Magento integration token, test on staging first, and require explicit confirmation before every write, delete, payment, shipment, cache flush, or custom API POST/PUT/DELETE action. <br>
Risk: Reports and customer workflows can expose customer and order data. <br>
Mitigation: Treat generated reports and customer details as sensitive, avoid exposing OAuth credentials in chat or logs, and limit output sharing to authorized users. <br>


## Reference(s): <br>
- [Magento 2 REST API Quick Reference](references/api-reference.md) <br>
- [Magento 2 Diagnostics Reference](references/diagnostics.md) <br>
- [AI Agent Workflow Reference](references/workflows.md) <br>
- [OpenClaw Magento 2 homepage](https://github.com/caravanglory/openclaw-magento2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown summaries with tables, definition lists, inline shell commands, and optional JSON from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only operations may run directly; write, delete, shipment, invoice, cache flush, and custom POST/PUT/DELETE actions require explicit confirmation.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
