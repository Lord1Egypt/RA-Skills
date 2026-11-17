## Description:

Helps agents read HODL.DANCE market data, simulate bonding-curve trades, execute BNB/token trades, and launch memecoins on the HODL.DANCE BSC launchpad.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hodldance](https://clawhub.ai/user/hodldance)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give agents a JSON-first CLI for discovering HODL.DANCE tokens, quoting bonding-curve trades, executing buy/sell transactions, and creating new tokens on BNB Chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write commands can spend real BNB, deploy tokens, approve token transfers, or sell tokens when a private key is configured.

Mitigation: Use a dedicated low-value wallet, run read and quote commands first, and require human approval with strict amount limits before buy-token, sell-token, or create-token.

Risk: The create-token command uploads a local logo file and token metadata.

Mitigation: Restrict logo paths to an approved directory and review metadata before allowing an agent to run create-token.

Risk: Unpinned npx execution may install a package version other than the reviewed release.

Mitigation: Pin @hodl-dance/skill to version 1.3.1 or install from a locked package source.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hodldance/skills/hodl-dance)
- [HODL.DANCE Documentation](https://docs.hodl.dance)
- [HODL.DANCE API](https://hodl.dance/api)
- [HODL.DANCE Agent Card](https://hodl.dance/.well-known/agent-card.json)
- [HODL.DANCE OpenAPI Spec](https://hodl.dance/.well-known/openapi.json)
- [NPM Package](https://www.npmjs.com/package/@hodl-dance/skill)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON to stdout, with command-line usage and environment variable guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write commands require HODL_PRIVATE_KEY and can submit BNB Chain transactions; read and quote commands do not require a wallet.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact package.json and CHANGELOG report 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
