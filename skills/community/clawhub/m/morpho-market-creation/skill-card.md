## Description: <br>
Deploys Morpho markets backed by API3 oracles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metobom](https://clawhub.ai/user/metobom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DeFi operators use this skill to collect Morpho market parameters, validate API3 oracle feeds, and choose a deployment path for creating an oracle-backed Morpho market. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadcast irreversible blockchain transactions. <br>
Mitigation: Prefer the Safe or Etherscan flow, and verify chain, contract addresses, oracle parameters, IRM, LLTV, wallet address, and gas impact before any transaction. <br>
Risk: The script flow asks for WALLET_MNEMONIC in a local environment file. <br>
Mitigation: Avoid putting a seed phrase in .env; if automation is unavoidable, use a dedicated low-fund deployer wallet. <br>
Risk: Incorrect oracle or market parameters can produce a misleading or unusable DeFi deployment. <br>
Mitigation: Review oracle-params.json and market-params.json, run oracle tests, and confirm API3 feed activity before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metobom/skills/morpho-market-creation) <br>
- [API3 Market](https://market.api3.org) <br>
- [Morpho Oracle Tester](https://oracles.morpho.dev/oracle-tester) <br>
- [Morpho Blue addresses](https://docs.morpho.org/get-started/resources/addresses/#morpho-blue) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pnpm and ts-node; script-based transaction flows require WALLET_MNEMONIC.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
