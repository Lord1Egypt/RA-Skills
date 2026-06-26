## Description: <br>
Use this skill when working with Kingdee K3Cloud ERP systems, including ERP document queries, sales and purchase orders, inventory, customers, suppliers, operational reports, field validation, MCP tool usage, and common Kingdee API troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamzhang1987](https://clawhub.ai/user/adamzhang1987) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to guide safe Kingdee K3Cloud ERP queries, reporting workflows, field-name validation, and controlled document operations through a configured MCP server. It helps agents retrieve or summarize ERP data and prepare operational reports while avoiding common form, field, pagination, and status-transition errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a configured Kingdee MCP server that may hold or access ERP credentials. <br>
Mitigation: Install and use it only with a trusted MCP server, confirm where credentials are stored, and avoid placing secrets in CLAUDE.md or other readable project notes. <br>
Risk: ERP exports and reports can contain sensitive business records. <br>
Mitigation: Treat exported files and generated reports as sensitive data, limit result sizes, and store or share them according to the organization's data handling rules. <br>
Risk: Create, submit, audit, unaudit, or batch actions can change ERP state. <br>
Mitigation: Require explicit user confirmation in the workflow before allowing an agent to perform state-changing ERP operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/adamzhang1987/kingdee-k3cloud) <br>
- [Recommended Kingdee K3Cloud MCP server](https://github.com/adamzhang1987/kingdee-k3cloud-mcp) <br>
- [Common errors](references/common-errors.md) <br>
- [Customer query guide](references/customer-query-guide.md) <br>
- [Customization guide](references/customization-guide.md) <br>
- [Daily report workflow](references/daily-report-workflow.md) <br>
- [General ledger voucher guide](references/gl-voucher-guide.md) <br>
- [Inventory analysis workflow](references/inventory-analysis-workflow.md) <br>
- [Order tracking workflow](references/order-tracking-workflow.md) <br>
- [Periodic report workflow](references/periodic-report-workflow.md) <br>
- [Sales analysis workflow](references/sales-analysis-workflow.md) <br>
- [Verified fields](references/verified-fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API calls, configuration, files] <br>
**Output Format:** [Markdown guidance with JSON-style MCP tool call examples and optional exported ERP data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agents should limit returned ERP rows, export large result sets to files, treat ERP exports as sensitive business records, and require explicit user confirmation before create, submit, audit, unaudit, or batch state-changing operations.] <br>

## Skill Version(s): <br>
1.3.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
