## Description:

Connects agents to Plisio to check balances and operations and create hosted invoices through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to retrieve Plisio balances and invoice or operation details, list operations, and create hosted invoices from a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute downloaded software and may affect other agent skills; the remote installers and hosted connector were not verified in this review.

Mitigation: Review and approve the CLI installation separately, use a verified release, and consider disabling automatic skill synchronization with the documented controls.

Risk: Creating a hosted invoice changes Plisio payment state, and OOMOL mediates access to the connected account.

Mitigation: Inspect the live action schema and confirm the exact invoice payload before running the create action.

## Reference(s):

- [Plisio API documentation](https://plisio.net/documentation)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-plisio)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON inputs and Plisio response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Invoice creation changes payment state; inspect the live action schema and confirm the exact invoice payload before execution.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
