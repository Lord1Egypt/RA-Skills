## Description:

Full-featured Odoo 17/18/19 ERP connector for OpenClaw, covering Sales, CRM, Purchase, Inventory, Projects, HR, Fleet, Manufacturing, and related business operations through a TypeScript plugin and XML-RPC integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuanle96](https://clawhub.ai/user/tuanle96)

### License/Terms of Use:


## Use Case:

Developers and business operators use this skill to connect OpenClaw agents to Odoo 17/18/19 for chat-driven ERP workflows such as sales, purchasing, inventory, invoicing, projects, HR, fleet, manufacturing, calendar, and eCommerce tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connector can make broad changes in an Odoo business system, including create, update, delete, post, confirm, and cancel operations.

Mitigation: Require human approval for state-changing actions and use a dedicated Odoo account with only the permissions needed for the intended workflow.

Risk: The install path is not pinned to reviewed code.

Mitigation: Verify the exact package source and version before installation and deployment.

Risk: Fuzzy find-or-create behavior may create unintended customers, products, projects, or other records.

Mitigation: Review matched and auto-created records before committing business-critical transactions.

Risk: The configured Odoo API key can grant access to sensitive business data and operations.

Mitigation: Protect the API key, rotate it if exposed, and avoid using broad administrator or accounting credentials.

## Reference(s):

- [OpenClaw Odoo Skill Page](https://clawhub.ai/tuanle96/skills/openclaw-odoo)
- [OpenClaw Odoo Repository](https://github.com/tuanle96/openclaw-odoo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, JSON configuration snippets, TypeScript code snippets, and natural-language ERP operation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform Odoo create, update, delete, post, confirm, cancel, and fuzzy find-or-create workflows when connected to a configured Odoo instance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
