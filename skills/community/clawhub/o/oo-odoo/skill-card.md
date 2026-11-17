## Description:

Use the oo CLI to read and manage Odoo records through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can search, inspect, create, update, and delete Odoo records through their connected account. The skill guides agents to check each action's live schema and seek approval for modifying or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions may run an online CLI installer whose implementation was not verified.

Mitigation: Verify the CLI source and review the installer before running it; do not automatically execute downloaded installers.

Risk: Some actions, including custom model methods and relational updates, can modify or delete Odoo data.

Mitigation: Use an account with only the required permissions, inspect the live action schema, and confirm the exact payload and effect before modifying or destructive actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Odoo](https://www.odoo.com)
- [Odoo External API documentation](https://www.odoo.com/documentation/18.0/developer/reference/external_api.html)

## Skill Output:

**Output Type(s):** [Odoo records and query results, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON payloads and results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include read-only queries and operations that can modify or delete records.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
