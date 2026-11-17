## Description:

Operate a connected Payrexx account to read transactions and gateways, list payment providers, and create payment gateways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Payrexx transaction and gateway data, list configured payment providers, or create checkout gateways through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs agents to run remote CLI installers that this artifact review did not verify.

Mitigation: Review and verify the CLI installer separately before running it.

Risk: Automatic CLI skill synchronization may be enabled, and gateway creation changes Payrexx account state.

Mitigation: Review the CLI synchronization setting and disable it if unwanted; confirm the checkout creation payload before creating a gateway.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Payrexx](https://payrexx.com)
- [Payrexx REST API documentation](https://developers.payrexx.com/reference/rest-api)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Payrexx data; gateway creation changes account state and requires user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
