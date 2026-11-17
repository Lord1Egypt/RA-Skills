## Description:

Manage Laravel Forge servers, sites, deployments, databases, integrations, and more via the Forge API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[florianbeer](https://clawhub.ai/user/florianbeer)

### License/Terms of Use:


## Use Case:

Developers and operators managing Laravel Forge infrastructure use this skill to inspect and change servers, sites, deployments, databases, credentials, teams, roles, recipes, backups, and related resources through Forge API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Forge API access can change infrastructure, deployments, databases, credentials, teams, roles, scheduled jobs, firewall rules, and remote commands.

Mitigation: Install only for trusted operators managing Forge infrastructure and require human review before delete, credential, role/team, deployment-script, scheduled-job, firewall, or remote-command operations.

Risk: Forge API tokens and related secrets may be exposed if passed directly on command lines or stored with broad filesystem permissions.

Mitigation: Use narrowly scoped tokens where possible, store credentials in the configured credentials file with owner-only permissions, and avoid passing secrets directly on the command line.

## Reference(s):

- [ClawHub Laravel Forge skill page](https://clawhub.ai/florianbeer/skills/laravel-forge)
- [Laravel Forge API reference introduction](https://forge.laravel.com/docs/api-reference/introduction)
- [Laravel Forge API documentation](https://forge.laravel.com/api-documentation)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON or plain-text API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and a Laravel Forge API token.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
