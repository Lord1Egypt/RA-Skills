## Description:

Guides agents in using @openserv-labs/client to manage OpenServ agents, workflows, triggers, tasks, provisioning, authentication, x402 payments, ERC-8004 identity, and Platform API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[issa-me-sush](https://clawhub.ai/user/issa-me-sush)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to provision and manage OpenServ Platform agents, workflows, triggers, credentials, payments, and on-chain identity from TypeScript projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys, API tokens, auth tokens, and webhook URLs may grant access to OpenServ resources if exposed.

Mitigation: Use a dedicated low-value wallet, keep .env and .openserv.json out of source control and logs, and treat generated webhook URLs as secrets.

Risk: Provisioning and PlatformClient examples create or update remote agents, workflows, triggers, credentials, and payment-enabled endpoints.

Mitigation: Review the requested resources, pin package and skill versions, and test with non-production accounts before applying changes to production projects.

Risk: Cleanup examples can delete OpenServ workflows and agents, including bulk deletion with --all.

Mitigation: Run cleanup commands only after verifying the authenticated account and target resource IDs.

Risk: ERC-8004 identity registration uses a funded Base wallet and may incur on-chain costs.

Mitigation: Fund only the intended wallet with limited ETH, wrap registration in error handling, and confirm chain and workflow details before submitting transactions.

## Reference(s):

- [OpenServ Client Skill Source](artifact/SKILL.md)
- [OpenServ Client API Reference](artifact/reference.md)
- [OpenServ Client Troubleshooting](artifact/troubleshooting.md)
- [OpenServ Client ClawHub Release](https://clawhub.ai/issa-me-sush/skills/openserv-client)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment-variable guidance, PlatformClient usage patterns, provisioning flows, trigger configuration, and cleanup commands.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
