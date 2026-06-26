## Description: <br>
Operate the LeadGenius Pro Automation API and lgp CLI for ICP management, FSD pipeline automation, lead generation, enrichment, scoring, user provisioning, territory analysis, webhooks, and email platform integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thierryteisseire](https://clawhub.ai/user/thierryteisseire) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Sales operations teams, revenue operations engineers, and agent developers use this skill to operate LeadGenius Pro lead-management workflows through API calls and lgp CLI commands. It supports customer onboarding, ICP setup, lead generation, enrichment, scoring, campaign delivery, administrative provisioning, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents privileged administrative, identity, database, transfer, deletion, backup, and purchasing operations. <br>
Mitigation: Use least-privilege API keys, test first against non-production data, and require explicit human approval before deletes, transfers, purchases, backups, or other privileged actions. <br>
Risk: The workflows may involve sensitive credentials such as LGP_ADMIN_KEY, Epsimo tokens, browser cookies, and account passwords. <br>
Mitigation: Keep privileged keys, tokens, cookies, and real passwords out of routine agent sessions; provide them only through approved secret-handling mechanisms when needed. <br>


## Reference(s): <br>
- [LeadGenius CLI project homepage](https://github.com/thierryteisseire/leadgenius-cli) <br>
- [LeadGenius Pro API](https://api.leadgenius.app) <br>
- [LeadGenius Pro documentation](https://api.leadgenius.app/docs) <br>
- [API Endpoints Reference](references/api_endpoints.md) <br>
- [LeadGenius Pro CLI Reference](references/cli_reference.md) <br>
- [Business Use Cases](references/use_cases.md) <br>
- [Workflow Reference](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands, HTTP examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; requires a LeadGenius Pro API key and separately obtained lgp CLI.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
