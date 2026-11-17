## Description:

CLI tool to create meme tokens on hot.fun (Solana). Returns structured JSON for token creation flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinxiuchen](https://clawhub.ai/user/qinxiuchen)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent users use this skill to collect token details, run the hotfun CLI, create a Solana meme token through the hot.fun API, sign the returned transaction, and submit it to Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses PRIVATE_KEY to sign and submit Solana transactions.

Mitigation: Use a dedicated low-balance wallet, never paste the private key into chat, and move remaining funds to a safer wallet after token creation.

Risk: The transaction is supplied by a remote token creation API before local signing.

Mitigation: Decode and independently verify the returned transaction before signing or submitting it on chain.

Risk: The documented install path uses mutable npm resolution such as @latest or npx.

Mitigation: Install a pinned package version and review the resolved package before exposing PRIVATE_KEY.

Risk: Project-local .env files can expose PRIVATE_KEY to unrelated tools or accidental commits.

Mitigation: Prefer scoped secret injection for the enabled skill and avoid storing PRIVATE_KEY in project-local .env files.

## Reference(s):

- [Hot.fun Create Token API Reference](references/api-create-token.md)
- [Hot Fun Integration on ClawHub](https://clawhub.ai/qinxiuchen/skills/hot-fun-ai)
- [qinxiuchen ClawHub Publisher Profile](https://clawhub.ai/user/qinxiuchen)
- [hot.fun token creation API endpoint](https://gate.game.com/v3/hotfun/agent/create_pool_with_config)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The create-token flow returns transaction hash, wallet, token mint, pool/config accounts, token metadata, image URL, and URI.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
