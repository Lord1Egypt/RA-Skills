## Description:

Operate Holded ERP through holdedcli to read and update data safely. Use when the user asks to read, search, create, update, or delete Holded entities (contacts, invoices, products, CRM, projects, team, accounting) or run Holded API endpoints from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaumecornado](https://clawhub.ai/user/jaumecornado)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to discover Holded ERP actions, inspect accepted parameters, and run read or confirmed write operations through holdedcli with structured JSON output. It is especially suited to workflows involving contacts, invoices, products, CRM, projects, team data, accounting records, and purchase receipt handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant broad access to financial ERP data through an unpinned third-party CLI.

Mitigation: Install only from trusted holdedcli sources and use a minimally scoped Holded API key.

Risk: Receipt creation may use --skip-validation, which can bypass client-side schema checks.

Mitigation: Review every write command before execution, especially purchase receipt creation, and confirm dates, taxes, and accounting rules before running it.

Risk: The documented accounting assumptions are focused on Spanish tenants.

Mitigation: Avoid applying the workflow to non-Spanish tenants unless local dates, taxes, and accounting rules are confirmed.

## Reference(s):

- [holded-skill homepage](https://github.com/jaumecornado/holded-skill)
- [Holded CLI Reference](references/holdedcli-reference.md)
- [holdedcli](https://github.com/jaumecornado/holdedcli)
- [Holded](https://www.holded.com)
- [Holded API key documentation](https://developers.holded.com/reference/api-key)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and JSON-oriented command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for explicit confirmation before write operations and summarizes IDs, HTTP status, and applied changes after execution.]

## Skill Version(s):

0.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
