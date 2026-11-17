## Description:

Full HubSpot platform CLI for CRM contacts, companies, deals, tickets, CMS blog posts and pages, marketing emails, forms, lists, conversations, and automation workflows using a Private App token or OAuth 2.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdelkrim](https://clawhub.ai/user/abdelkrim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and CRM administrators use this skill to inspect and manage HubSpot CRM, CMS, marketing, conversations, and workflow resources from an agent-assisted CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, or delete sensitive HubSpot CRM and business records when granted write scopes.

Mitigation: Use a least-privilege HubSpot Private App token, grant write scopes only for required workflows, and require human review before running destructive or bulk-changing commands.

Risk: OAuth mode caches a temporary access token locally in plaintext.

Mitigation: Prefer Private App token mode when practical, restrict local machine access, and remove ~/.cache/openclaw/hubspot-token.json when OAuth access is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abdelkrim/skills/hubspot-by-altf1be)
- [HubSpot developer documentation](https://developers.hubspot.com/)
- [HubSpot API coverage and limitations](docs/API-COVERAGE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI output from HubSpot API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require HubSpot credentials and may read or modify CRM, CMS, marketing, conversations, and workflow records.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
