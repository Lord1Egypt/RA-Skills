## Description:

Use when an OpenClawBot needs to create or verify PayTrigo payments on Base/USDC without webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paytrigo](https://clawhub.ai/user/paytrigo)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to help OpenClawBots create PayTrigo invoices, route users to browser payment, perform direct bot payment, submit transaction hashes, and poll payment status on Base/USDC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release embeds live PayTrigo payment API keys.

Mitigation: Install only after the publisher removes and rotates embedded keys and requires user- or deployment-provided secrets.

Risk: The bot payment flow can sign blockchain transactions from a user's wallet without enough decoded transaction validation or explicit confirmation.

Mitigation: Require decoded transaction review and explicit confirmation before bot payments; use a dedicated low-balance wallet when testing.

Risk: Private keys and passphrases can be supplied on the command line.

Mitigation: Avoid raw command-line secrets; prefer protected secret files or deployment secret stores with restrictive filesystem permissions.

Risk: Dependencies are not pinned with a lockfile.

Mitigation: Add and review a lockfile before deployment so dependency resolution is repeatable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paytrigo/skills/paytrigo-openclawbot)
- [PayTrigo API endpoint](https://api.paytrigo.net)
- [Base mainnet RPC endpoint](https://mainnet.base.org)
- [Artifact README](README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts can produce JSON API responses, local wallet files, and on-chain transaction hashes when executed.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
