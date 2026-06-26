## Description: <br>
Trade, create, and manage memecoins on HODL.DANCE's BSC bonding curve launchpad. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hodldance](https://clawhub.ai/user/hodldance) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, agents, and trading bot operators use this skill to query HODL.DANCE token data, simulate trades, execute buy and sell transactions, and launch tokens on BSC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend real crypto funds and approve token transfers from a BSC wallet. <br>
Mitigation: Use a low-balance dedicated wallet, run quote commands before transactions, and require manual review before buy, sell, approve, or create commands execute. <br>
Risk: Incorrect contract addresses or amounts can lead to unintended trades or token approvals. <br>
Mitigation: Manually verify bonding curve addresses, token addresses, transaction amounts, and expected output before signing. <br>
Risk: The skill requires a private key for create-token, buy-token, and sell-token commands. <br>
Mitigation: Store HODL_PRIVATE_KEY only in a controlled local environment and do not expose it in prompts, logs, shared terminals, or unattended agent runs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hodldance/hodl-dance) <br>
- [HODL.DANCE Documentation](https://docs.hodl.dance) <br>
- [HODL.DANCE API](https://hodl.dance/api) <br>
- [HODL.DANCE Agent Card](https://hodl.dance/.well-known/agent-card.json) <br>
- [HODL.DANCE OpenAPI Spec](https://hodl.dance/.well-known/openapi.json) <br>
- [NPM Package](https://www.npmjs.com/package/@hodl-dance/skill) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, API calls] <br>
**Output Format:** [JSON to stdout from CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include token metadata, trade quotes, transaction hashes, gas usage, approval status, and structured error codes.] <br>

## Skill Version(s): <br>
1.3.1 (source: ClawHub release metadata; artifact package.json, README, and CHANGELOG list 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
