## Description:

CLI tool to create meme tokens on hot.fun on Solana and return structured JSON for the token creation flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinxiuchen](https://clawhub.ai/user/qinxiuchen)

### License/Terms of Use:

MIT

## Use Case:

External developers and operators use this skill to create meme tokens on Solana through the hotfun CLI after collecting token details and confirming wallet and private-key risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses a Solana PRIVATE_KEY and signs a transaction supplied by the hot.fun API.

Mitigation: Use a fresh low-value Solana wallet, do not paste or share the private key in chat, and independently verify the exact transaction contents and expected on-chain effects before signing.

Risk: Mutable npm installation paths such as npx or @latest can change the code executed by the agent.

Mitigation: Pin the npm package version, review the package before use, and avoid npx or @latest for this workflow.

Risk: Storing real wallet keys in shared project environment files can expose funds.

Mitigation: Avoid storing production wallet keys in shared .env files and move funds out of the operating wallet promptly after use.

## Reference(s):

- [Hot.fun Create Token API Reference](artifact/references/api-create-token.md)
- [ClawHub skill page](https://clawhub.ai/qinxiuchen/skills/hot-fun-integration)
- [hot.fun create token API endpoint](https://gate.game.com/v3/hotfun/agent/create_pool_with_config)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with shell command invocations and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The command output includes transaction hash, wallet, token mint, pool/config accounts, token name and symbol, image URL, and metadata URI.]

## Skill Version(s):

1.0.1 (source: evidence.release.version; artifact metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
