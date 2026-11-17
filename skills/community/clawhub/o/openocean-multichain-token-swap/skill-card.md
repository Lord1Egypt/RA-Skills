## Description:

OpenOcean-skills is a skill package for interacting with the OpenOcean Aggregator API to get swap quotes, build swap transactions, execute swaps, and troubleshoot OpenOcean workflows across 40+ chains, including EVM, Solana, and Sui.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openocean-admin](https://clawhub.ai/user/openocean-admin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve OpenOcean swap quotes, build transaction calldata, execute confirmed or automated swaps, and troubleshoot token swap failures across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fast execution path can immediately broadcast real blockchain transactions without a confirmation step.

Mitigation: Prefer quote, swap-build, and confirmed swap-execute flows; use swap-execute-fast only for intentional unattended automation with a dedicated low-balance wallet and narrow token allowances.

Risk: The security evidence reports unsafe shell-script patterns in the execution scripts.

Mitigation: Review and fix the eval and Python interpolation issues before running scripts, and independently verify router and chain details.

Risk: On-chain swaps are irreversible and can incur gas costs even when a transaction fails.

Mitigation: Test with small amounts, verify balances and token allowances, use conservative slippage, and monitor gas before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openocean-admin/skills/openocean-multichain-token-swap)
- [OpenOcean Homepage](https://openocean.finance)
- [OpenOcean API Documentation](https://apis.openocean.finance/)
- [OpenOcean API Reference](artifact/references/api-reference.md)
- [OpenOcean Token Registry](artifact/references/token-registry.md)
- [Basic Quote Example](artifact/skills/quote/references/basic-quote.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON transaction payloads and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include swap quotes, token addresses, transaction calldata, router addresses, gas estimates, transaction hashes, and troubleshooting guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
