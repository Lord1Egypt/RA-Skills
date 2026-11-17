## Description:

NaviOffice Skill helps agents query and operate NaviOffice OA modules for system administration, HR, attendance, finance, CRM, sales, purchasing, inventory, projects, production, and calibration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaowb82](https://clawhub.ai/user/zhaowb82)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business operations teams use this skill through an authorized agent to retrieve NaviOffice records and prepare supported business actions across office, CRM, finance, inventory, production, and project modules. It is intended for environments where the agent is allowed to access live NaviOffice business data with a scoped API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive NaviOffice HR, finance, CRM, inventory, production, and project data.

Mitigation: Use a least-privilege, revocable API token and confirm the agent should access each enabled NaviOffice module before deployment.

Risk: Raw API clients and custom API URL configuration can send the user's API token to unintended destinations.

Mitigation: Keep requests on trusted HTTPS NaviOffice hosts and allow custom domains only after explicit review.

Risk: The shell client can load credentials from an untrusted or automatically generated .env file.

Mitigation: Use only reviewed environment files and avoid the shell client when the .env source is not trusted.

## Reference(s):

- [System Management Reference](references/system.md)
- [Human Resources Reference](references/hr.md)
- [Attendance Reference](references/attendance.md)
- [Finance Reference](references/finance.md)
- [CRM Reference](references/crm.md)
- [CRM API Reference](references/crm-api.md)
- [Sales Reference](references/sales.md)
- [Purchase Reference](references/purchase.md)
- [Inventory Reference](references/inventory.md)
- [Project Reference](references/project.md)
- [Production Reference](references/mes.md)
- [Calibration Reference](references/calibration.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NAVI_OFFICE_API_TOKEN; optional API URL configuration defaults to the NaviOffice endpoint documented by the artifact.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
