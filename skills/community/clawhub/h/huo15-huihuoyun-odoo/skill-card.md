## Description:

Huo15 Huihuoyun Odoo lets an agent use natural language to operate Huihuoyun/Odoo ERP workflows across tasks, CRM, projects, helpdesk, finance, sales, HR, inventory, manufacturing, customer service, knowledge, and Studio-style administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, implementation managers, project managers, sales managers, and operations teams use this skill to query and update Huihuoyun/Odoo ERP records through an OpenClaw agent. It supports daily briefings, task and activity management, CRM pipeline work, sales and purchase review, invoices, helpdesk tickets, HR, inventory, notifications, and administrative workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad ERP, administration, Studio, automation, report scheduling, CSV import, webhook, arbitrary file-upload, and local-file capabilities to an agent.

Mitigation: Have an administrator review the enabled tool tier before installation and disable capabilities that are unnecessary for the deployment.

Risk: The skill handles ERP credentials and can be configured in ways that over-share privileged accounts.

Mitigation: Use low-privilege per-user ERP accounts, avoid shared administrator credentials, and use protected secret handling instead of ordinary chat for passwords when available.

Risk: The skill connects to external ERP origins and performs background polling or automation.

Mitigation: Require HTTPS allowlisted ERP origins and review polling channels, intervals, and automation scope before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/skills/huo15-huihuoyun-odoo)
- [Huihuoyun Website](https://www.huo15.com)
- [OpenClaw Project](https://github.com/nicepkg/openclaw)
- [Huo15 Companion Videos](https://space.bilibili.com/400418085)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool-call descriptions, configuration snippets, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute ERP actions through configured OpenClaw tools; users should review actions that modify business records.]

## Skill Version(s):

1.23.2 (source: server release evidence and package.json; SKILL.md frontmatter reports 1.23.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
