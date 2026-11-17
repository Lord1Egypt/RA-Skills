## Description:

Kustomer (kustomer.com). Use this skill for ANY Kustomer request — reading, creating, and updating data. Whenever a task involves Kustomer, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support teams use this skill to retrieve, search, create, and update Kustomer customer records through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run a remote installer without separate approval or clear limits on local changes, and CLI synchronization can update local skills.

Mitigation: Review and approve dependency installation separately, use a verified CLI release, and review or disable automatic skill synchronization.

Risk: The connected OOMOL account mediates access to customer data, and create or update actions can change records.

Mitigation: Grant only the permissions needed and confirm the exact changes before running write actions.

## Reference(s):

- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)
- [Kustomer](https://www.kustomer.com)
- [Kustomer API documentation](https://developer.kustomer.com/kustomer-api-docs/reference)
- [Kustomer on ClawHub](https://clawhub.ai/oomol/skills/oo-kustomer)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations retrieve customer data; create_customer and update_customer change customer records.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
