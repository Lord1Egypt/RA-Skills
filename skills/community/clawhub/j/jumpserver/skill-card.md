## Description:

JumpServer V4.10 query and analysis skill for assets, accounts, users, organizations, permissions, audit activity, diagnostics, governance inspection, and usage reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibuler](https://clawhub.ai/user/ibuler)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, JumpServer administrators, and auditors use this skill to query JumpServer inventory, permissions, and audit data, run configuration diagnostics, inspect governance posture, and generate daily or time-range usage reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and privileged JumpServer audit data may be exposed if the skill is installed for unauthorized users or used with overly broad query scope.

Mitigation: Install only for authorized JumpServer administrators or auditors, and limit queries and reports to the minimum organization, time range, and fields needed.

Risk: Insecure transport defaults can weaken protection for credentials and audit data.

Mitigation: Require HTTPS, enable TLS verification, and avoid password authentication over insecure transport.

Risk: Automatic dependency installation and persistent local configuration writes can change the runtime environment or store sensitive settings locally.

Mitigation: Pin and preinstall dependencies, store secrets outside the repository when possible, and review .env writes and organization changes before confirming.

## Reference(s):

- [README.en.md](README.en.md)
- [Routing Playbook](references/routing-playbook.md)
- [Runtime](references/runtime.md)
- [Safety Rules](references/safety-rules.md)
- [Report Template Playbook](references/report-template-playbook.md)
- [Capabilities](references/capabilities.md)
- [Permissions](references/permissions.md)
- [Audit](references/audit.md)
- [Diagnose](references/diagnose.md)
- [Daily Usage Report Template Fields](references/metadata/daily_usage_report_template_fields.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, HTML files, guidance]

**Output Format:** [Markdown responses with command summaries, JSON-like query results, configuration guidance, and generated HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local .env, organization context, and reports/JumpServer-YYYY-MM-DD.html when confirmed by the workflow.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
