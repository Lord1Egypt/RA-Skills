## Description:

Operate the LeadGenius Pro Automation API and lgp CLI - ICP management, FSD pipeline automation, lead generation/enrichment/scoring, user provisioning, territory analysis, webhooks, and email platform integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thierryteisseire](https://clawhub.ai/user/thierryteisseire)

### License/Terms of Use:

MIT

## Use Case:

Sales operations teams, developers, and AI agents use this skill to operate LeadGenius Pro lead-management workflows, including ICP setup, lead generation, enrichment, scoring, qualification, user provisioning, webhook handling, and email-platform delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill teaches broad admin, deletion, backup, credential-handling, role, and cross-company operations over LeadGenius production data.

Mitigation: Install only for trusted agents and users; test destructive table, user, company, backup, and PITR operations in staging before using them on production data.

Risk: The optional LGP_ADMIN_KEY grants elevated behavior including rate-limit bypass and privileged admin workflows.

Mitigation: Do not grant LGP_ADMIN_KEY unless admin backup, restore, role, or cross-company operations are required.

Risk: Token and password handling appears in documented commands and API examples.

Mitigation: Prefer environment variables or a secret manager over command-line token or password flags, and avoid token query parameters.

## Reference(s):

- [LeadGenius CLI ClawHub Skill Page](https://clawhub.ai/thierryteisseire/skills/leadgenius-cli)
- [ClawHub Metadata Homepage](https://github.com/thierryteisseire/leadgenius-cli)
- [LeadGenius Pro API Documentation](https://api.leadgenius.app/docs)
- [API Endpoints Reference](references/api_endpoints.md)
- [CLI Reference](references/cli_reference.md)
- [Business Use Cases](references/use_cases.md)
- [Workflow Reference](references/workflows.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration]

**Output Format:** [Markdown guidance with CLI commands, API examples, and configuration tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; the lgp CLI is not included and LeadGenius API access requires LGP_API_KEY.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
