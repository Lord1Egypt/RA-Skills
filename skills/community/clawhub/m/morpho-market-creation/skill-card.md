## Description: <br>
Deploys Morpho markets backed by Api3 oracles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metobom](https://clawhub.ai/user/metobom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DeFi operators use this skill to validate Api3 feeds, deploy a Morpho oracle, and create a Morpho market with guided checks before transactions are submitted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a local wallet mnemonic to submit irreversible blockchain transactions. <br>
Mitigation: Use a dedicated low-value deployment wallet, never a primary seed phrase, and prefer the Safe or Etherscan paths when possible. <br>
Risk: Incorrect chain, token, oracle, IRM, LLTV, gas, or contract address values can create an unintended or unsafe market. <br>
Mitigation: Independently verify all deployment parameters and contract addresses before approving any transaction. <br>
Risk: Api3 reader proxy addresses and ERC-20 token contract addresses serve different roles and may be confused during setup. <br>
Mitigation: Confirm oracle feed addresses in the oracle parameters and separately confirm ERC-20 token addresses in the market parameters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metobom/skills/morpho-market-creation) <br>
- [Api3 Market integration pages](https://market.api3.org/) <br>
- [Morpho Oracle Tester](https://oracles.morpho.dev/oracle-tester) <br>
- [Morpho Blue addresses](https://docs.morpho.org/get-started/resources/addresses/#morpho-blue) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration edits, URLs, transaction hashes, and deployed contract identifiers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pnpm, ts-node, and WALLET_MNEMONIC when using the script-based transaction path.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
