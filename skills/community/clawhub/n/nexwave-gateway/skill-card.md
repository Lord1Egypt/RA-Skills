## Description:

Nexwave Gateway helps OpenClaw agents use Circle Gateway and Circle Programmable Wallets to check unified testnet USDC balances, deposit USDC, and mint USDC across supported EVM testnets without raw private keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[botmechanic](https://clawhub.ai/user/botmechanic)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent builders use this skill to give OpenClaw agents a unified USDC workflow across supported Circle Gateway testnets. It provides setup guidance and scripts for balance checks, deposits, burn-intent signing, attestation requests, and testnet minting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Circle API and entity secrets that can authorize wallet and transaction operations.

Mitigation: Use a limited testnet Circle account, restrict wallet sets to the intended chains, and keep credentials out of shared terminals and logs.

Risk: The setup flow installs unpinned npm dependencies before running the gateway scripts.

Mitigation: Review dependencies and pin them with a lockfile before using the setup output in a persistent environment.

Risk: Wallet initialization can create missing Circle wallets in the configured wallet set.

Mitigation: Run balance checks only against wallet sets where automatic testnet wallet creation is acceptable.

Risk: The deposit and transfer scripts approve, deposit, sign burn intents, request attestations, and mint hardcoded testnet USDC amounts.

Mitigation: Inspect configured amounts, source chains, destination chains, and recipient addresses before running transaction scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/botmechanic/skills/nexwave-gateway)
- [Circle Gateway Docs](https://developers.circle.com/gateway)
- [Circle Programmable Wallets](https://developers.circle.com/wallets)
- [Gateway Quickstart](https://developers.circle.com/gateway/quickstarts/unified-balance-evm)
- [Gateway Quickstart Code](https://github.com/circlefin/evm-gateway-contracts/tree/master/quickstart)
- [Arc Testnet Docs](https://docs.arc.network)
- [Circle Wallet Skill](https://clawhub.ai/eltontay/circle-wallet)
- [Gateway API Reference](https://gateway-api-testnet.circle.com/v1/info)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash and JavaScript examples; runtime scripts print console text and transaction hashes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Circle API credentials, a Circle wallet set, Node.js dependencies, and testnet USDC/gas on the supported networks.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
