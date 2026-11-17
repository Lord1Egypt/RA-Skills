## Description:

Guides agents through Kingdee K3Cloud ERP queries, document operations, reporting workflows, field validation, and API troubleshooting using a configured MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamzhang1987](https://clawhub.ai/user/adamzhang1987)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and ERP operators use this skill to query Kingdee K3Cloud sales, purchasing, inventory, customer, supplier, voucher, and reporting data and to prepare controlled ERP document actions such as save, submit, audit, and unaudit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ERP record changes such as save, submit, audit, and unaudit can affect operational records.

Mitigation: Use query-only MCP credentials by default and require explicit confirmation before any write or approval action.

Risk: Bulk approvals or broad exports can expose or change large volumes of sensitive ERP and customer data.

Mitigation: Scope queries and actions narrowly, avoid bulk approvals unless separately approved, export only to approved paths with restricted permissions, and clean up files.

Risk: Incorrect form IDs, field names, or document numbers can return wrong data or target wrong records.

Mitigation: Verify exact form IDs, fields, and document numbers with metadata or detail queries before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adamzhang1987/skills/kingdee-k3cloud)
- [Recommended Kingdee K3Cloud MCP Server](https://github.com/adamzhang1987/kingdee-k3cloud-mcp)
- [Customization Guide](references/customization-guide.md)
- [Customer Query Guide](references/customer-query-guide.md)
- [Order Tracking Workflow](references/order-tracking-workflow.md)
- [Common Errors](references/common-errors.md)
- [Daily Report Workflow](references/daily-report-workflow.md)
- [Sales Analysis Workflow](references/sales-analysis-workflow.md)
- [Inventory Analysis Workflow](references/inventory-analysis-workflow.md)
- [Verified Fields](references/verified-fields.md)
- [Periodic Report Workflow](references/periodic-report-workflow.md)
- [GL Voucher Guide](references/gl-voucher-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with MCP tool-call examples, JSON snippets, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend writing large ERP query results to CSV, Excel, or NDJSON files instead of returning them inline.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
