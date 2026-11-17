## Description:

Integrates with Harvest API v2 to help agents work with time entries, projects, tasks, clients, user assignments, invoices, expenses, reports, company records, and roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachgodsell93](https://clawhub.ai/user/zachgodsell93)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to give an agent Harvest API reference guidance for time reporting, project administration, invoicing-related workflows, expense reporting, and account management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes broad Harvest business, financial, and account-changing actions.

Mitigation: Install only for agents that should access Harvest, use a least-privileged Harvest token, and avoid broad admin tokens where possible.

Risk: Agent-guided requests can create, update, delete, send invoices, or change company and account records.

Mitigation: Require explicit user confirmation before write operations, invoice sending, company updates, or account-record changes.

## Reference(s):

- [Harvest Developer Access Setup](https://id.getharvest.com/developers)
- [Harvest API v2 Base URL](https://api.harvestapp.com/v2)
- [ClawHub Skill Page](https://clawhub.ai/zachgodsell93/skills/harvest-time-reporting-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown API reference with cURL examples and environment-variable setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses HARVEST_ACCESS_TOKEN and HARVEST_ACCOUNT_ID for authenticated Harvest API requests.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
