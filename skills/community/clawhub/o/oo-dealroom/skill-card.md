## Description:

Search Dealroom companies, investors, and transactions through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Dealroom users and analysts can search company, investor, and transaction data through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute downloaded CLI installer code whose source has not been verified.

Mitigation: Review and approve the CLI installation separately, and use a verified release where possible.

Risk: The skill uses automatic skill synchronization and an external hosted connector implementation that has not been verified.

Mitigation: Connect only the Dealroom account intended for this use and review the external components before relying on them.

## Reference(s):

- [Dealroom API documentation](https://docs.dealroom.co/docs/premium-api)
- [Dealroom](https://dealroom.co)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured Dealroom results with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on the connected Dealroom account and the selected action's input schema.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
