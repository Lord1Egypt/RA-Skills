## Description:

Manage Hostinger account services through API commands for VPS, DNS, domains, websites, hosting, Docker, firewalls, snapshots, backups, and billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rexlunae](https://clawhub.ai/user/rexlunae)

### License/Terms of Use:


## Use Case:

Developers and site operators use this skill to inspect and manage Hostinger infrastructure and account resources from an agent workflow. It supports operational tasks such as VPS lifecycle changes, DNS updates, Docker deployments, firewall configuration, domain management, and billing lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate with a broad Hostinger API token and make account-changing requests.

Mitigation: Use the least-privileged token Hostinger supports and review DNS, billing, domain, VPS, firewall, SSH key, Docker, delete, reset, restore, recreate, and curl commands before execution.

Risk: Root passwords or API tokens could appear in command lines, logs, or shell history.

Mitigation: Avoid passing root passwords on the command line and rotate any password or token that may have appeared in logs or shell history.

## Reference(s):

- [Hostinger Skill Page](https://clawhub.ai/rexlunae/skills/hostinger)
- [Hostinger API Endpoints](references/api-endpoints.md)
- [Hostinger API Reference](https://developers.hostinger.com)
- [Hostinger API Token Page](https://hpanel.hostinger.com/profile/api)
- [Hostinger OpenAPI Specification](https://github.com/hostinger/api/blob/main/openapi.json)
- [Hostinger Python SDK](https://github.com/hostinger/api-python-sdk)
- [Hostinger CLI Tool](https://github.com/hostinger/api-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output may include Hostinger API command invocations and JSON payload examples that require review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
