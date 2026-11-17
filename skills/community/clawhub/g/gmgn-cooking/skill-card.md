## Description:

Helps agents create and launch meme coins and crypto tokens on supported launchpads, or query launchpad creation statistics, through GMGN CLI/API workflows on Solana, BSC, and Base with explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmgnai](https://clawhub.ai/user/gmgnai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare confirmed GMGN CLI commands for token launches on supported launchpads, including chain, launchpad, image, slippage, fee-share, buyback, and auto-sell settings. It can also query token creation statistics by launchpad.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token creation spends real funds and can deploy irreversible on-chain contracts.

Mitigation: Require explicit confirmation before each create command, use a dedicated low-balance wallet, and reconfirm launch parameters before execution.

Risk: GMGN API keys and private keys can authorize real financial actions if mishandled.

Mitigation: Keep credentials in the GMGN user config, avoid project-level .env files that shadow or expose secrets, and never display or log secret values.

Risk: Global installation of gmgn-cli may use an unexpected package or version.

Mitigation: Review the gmgn-cli package and version before installing or updating it globally.

Risk: Fee-share, buyback, and auto-sell settings can permanently route funds or trigger automated trades.

Mitigation: Reconfirm every fee-share, buyback, and auto-sell option with the user before launch.

## Reference(s):

- [GMGN Skill Cooking on ClawHub](https://clawhub.ai/gmgnai/skills/gmgn-cooking)
- [GMGN API key setup](https://gmgn.ai/ai)
- [gmgn-swap related skill](https://github.com/GMGNAI/gmgn-skills/tree/main/skills/gmgn-swap)
- [gmgn-token related skill](https://github.com/GMGNAI/gmgn-skills/tree/main/skills/gmgn-token)
- [gmgn-market related skill](https://github.com/GMGNAI/gmgn-skills/tree/main/skills/gmgn-market)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can initiate real blockchain transactions only after explicit user confirmation; status polling may report order state, transaction hash, block explorer links, and output token address.]

## Skill Version(s):

1.4.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
