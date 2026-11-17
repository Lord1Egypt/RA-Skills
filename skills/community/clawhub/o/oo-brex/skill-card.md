## Description:

Search and read Brex data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and finance teams use this skill to search and read Brex company, user, budget, card account, expense, and settled transaction data through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded code without a clear approval step.

Mitigation: Review and approve CLI installation separately, and verify the installer and its skill synchronization behavior before enabling automatic setup.

Risk: The connected service may process financial data and hold connection credentials.

Mitigation: Use limited Brex permissions and assess whether OOMOL should process the financial data and hold the connection credentials.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-brex)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Brex](https://www.brex.com/)
- [Brex authentication documentation](https://developer.brex.com/guides/authentication)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON inputs and responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations return Brex data through the connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
