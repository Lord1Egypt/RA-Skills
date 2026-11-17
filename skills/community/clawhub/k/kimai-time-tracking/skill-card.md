## Description:

Provides a Kimai time-tracking CLI integration for managing timesheets, customers, projects, activities, teams, invoices, exports, and system queries through the Kimai REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x7466](https://clawhub.ai/user/0x7466)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to automate Kimai time-tracking workflows, inspect and export timesheet data, and manage Kimai entities through a CLI-backed REST API integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Kimai API token that may grant access to sensitive time-tracking and administrative data.

Mitigation: Use a dedicated least-privilege token, avoid administrator tokens, and set KIMAI_BASE_URL only to a trusted HTTPS Kimai host.

Risk: Delete commands can remove Kimai records and may cascade to related projects, activities, or timesheets.

Mitigation: Review the affected records before destructive actions and avoid --force unless the deletion has been explicitly confirmed.

Risk: Server security evidence says the skill overstates some capabilities and that some documented commands or safety features may be missing.

Mitigation: Verify required commands against a non-production Kimai instance before relying on the skill for operational workflows.

Risk: Timesheet exports and CLI output can contain personal, customer, project, or billing information.

Mitigation: Keep exports in controlled workspaces and redact sensitive data before sharing command output or generated files.

## Reference(s):

- [Kimai Time Tracking on ClawHub](https://clawhub.ai/0x7466/skills/kimai-time-tracking)
- [Kimai](https://www.kimai.org/)
- [Kimai REST API Docs](https://www.kimai.org/documentation/rest-api.html)
- [Kimai API Pagination Guide](https://www.kimai.org/documentation/api-pagination.html)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI responses may be JSON, tables, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KIMAI_BASE_URL and KIMAI_API_TOKEN; operations depend on the token's Kimai API permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata and script VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
