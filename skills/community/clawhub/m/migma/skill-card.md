## Description:

Generate, send, validate, and export AI-powered emails from the terminal; manage contacts, segments, tags, domains, and webhooks with Migma CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamsey](https://clawhub.ai/user/adamsey)

### License/Terms of Use:


## Use Case:

Marketing teams, operators, and developers use this skill to generate branded email campaigns, validate deliverability, send individual or bulk emails, export to ESPs, and manage contacts, segments, tags, domains, and webhooks through Migma CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable real bulk-email sends and contact-list mutations without enough built-in safeguards.

Mitigation: Require the agent to show recipients, audience counts, sender, subject, and content before any real send or contact-list change.

Risk: A Migma API key can authorize sensitive email and contact operations.

Mitigation: Use a scoped, rotatable Migma API key and pin or verify the @migma/cli package where possible.

Risk: CSV imports and contact removals can affect sensitive contact data.

Mitigation: Require explicit confirmation and maintain backups or auditability for contact imports and removals.

## Reference(s):

- [Migma homepage](https://migma.ai)
- [ClawHub skill page](https://clawhub.ai/adamsey/skills/migma)
- [Example Conversations](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Migma CLI commands and JSON-oriented command expectations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the migma CLI and a MIGMA_API_KEY for live Migma operations.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
