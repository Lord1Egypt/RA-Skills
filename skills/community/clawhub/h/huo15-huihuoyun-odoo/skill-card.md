## Description: <br>
Connects an OpenClaw agent to the Huo15 Huihuoyun/Odoo ERP suite so users can manage CRM, tasks, projects, tickets, sales, purchasing, finance, HR, inventory, approvals, messages, reports, and Studio workflows through natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and implementation, project, sales, support, finance, inventory, and HR teams use this skill to operate Huihuoyun/Odoo business records through an agent while preserving per-user Odoo permissions. It is intended for ERP workflows such as daily briefings, task management, CRM follow-up, orders, invoices, approvals, notifications, and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority over sensitive ERP records and workflows. <br>
Mitigation: Use per-user, least-privilege Odoo accounts and review the skill before installation. <br>
Risk: Shared or administrator credentials could bypass intended Odoo role-based access controls. <br>
Mitigation: Avoid shared admin credentials; keep the default per-user credential isolation unless a shared read-only account is intentionally required. <br>
Risk: Background sync and automation features may expose or act on business data without a user actively requesting each check. <br>
Mitigation: Disable unneeded sync channels and protect the OpenClaw plugin configuration directory. <br>
Risk: High-impact actions such as payments, purchases, user or group changes, bulk edits, webhooks, scheduled reports, and outbound email can affect business operations. <br>
Mitigation: Require human confirmation before executing these actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhaobod1/huo15-huihuoyun-odoo) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [package.json](package.json) <br>
- [OpenClaw](https://github.com/nicepkg/openclaw) <br>
- [Huo15 Huihuoyun service](https://www.huo15.com) <br>
- [Bilibili support videos](https://space.bilibili.com/400418085) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Agent-facing text and structured tool results rendered into conversational responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ERP record identifiers, dates, monetary totals, order or invoice summaries, notification counts, links to ERP records, and connection status.] <br>

## Skill Version(s): <br>
1.23.2 (source: server release metadata and package.json; SKILL.md and openclaw.plugin.json list 1.23.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
