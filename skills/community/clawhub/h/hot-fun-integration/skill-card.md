## Description: <br>
CLI tool to create meme tokens on hot.fun (Solana) and return structured JSON for the token creation flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinxiuchen](https://clawhub.ai/user/qinxiuchen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to create Solana meme tokens through the hotfun CLI after collecting token metadata and confirming wallet-use requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI receives full signing authority through PRIVATE_KEY. <br>
Mitigation: Use a fresh low-balance wallet for this skill and never paste or expose the private key in chat. <br>
Risk: The command signs and broadcasts a transaction returned by a remote API. <br>
Mitigation: Require a decoded transaction preview before allowing signing or broadcast. <br>
Risk: The install path can fetch npm package code at runtime when using @latest or npx auto-install. <br>
Mitigation: Install only from a trusted package source and prefer a pinned, reviewed package version. <br>


## Reference(s): <br>
- [Hot.fun Create Token API Reference](artifact/references/api-create-token.md) <br>
- [Hot Fun Integration on ClawHub](https://clawhub.ai/qinxiuchen/hot-fun-integration) <br>
- [hot.fun create_pool_with_config API](https://gate.game.com/v3/hotfun/agent/create_pool_with_config) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; create-token returns JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Token creation output includes transaction hash, wallet, mint address, pool/config accounts, token name, symbol, image URL, and metadata URI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; skill frontmatter metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
