## Description:

Deploys Morpho markets backed by Api3 oracles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api3dao](https://clawhub.ai/user/api3dao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DeFi operators use this skill to configure, validate, and deploy Morpho markets backed by Api3 oracle feeds, including oracle checks and transaction execution options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadcast irreversible blockchain transactions for oracle deployment and Morpho market creation.

Mitigation: Use Safe or Etherscan when possible, verify chain IDs, contract addresses, oracle feeds, IRM, LLTV, gas costs, and transaction targets before approving any transaction.

Risk: The script execution path uses WALLET_MNEMONIC from a local environment file.

Mitigation: Use a dedicated low-value deployment account, never use a production seed phrase, and avoid installing dependencies after secrets are placed in the project.

Risk: Incorrect token, oracle, or feed addresses can create an unusable or unsafe market.

Mitigation: Validate Api3ReaderProxyV1 addresses, run the Morpho Oracle Tester, and confirm token addresses are ERC-20 token contracts rather than oracle proxy addresses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/api3dao/skills/morpho-market-creation)
- [Api3 Market](https://market.api3.org/)
- [Morpho Oracle Tester](https://oracles.morpho.dev/oracle-tester)
- [Morpho Blue Addresses](https://docs.morpho.org/get-started/resources/addresses/#morpho-blue)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and configuration file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pnpm, ts-node, WALLET_MNEMONIC, and completed oracle and market parameter JSON files.]

## Skill Version(s):

0.6.0 (source: SKILL.md metadata and server release evidence; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
