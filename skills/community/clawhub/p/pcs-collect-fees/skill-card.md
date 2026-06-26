## Description: <br>
Check and collect LP fees from PancakeSwap V3 and Infinity (v4) positions, including pending fees, uncollected fees, harvest requests, and token-pair-specific fee checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcs-bot](https://clawhub.ai/user/pcs-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect PancakeSwap liquidity positions, estimate pending fees, and receive PancakeSwap deep links for reviewing and collecting fees in a wallet-controlled UI. The skill is intended for read-only position discovery and fee summaries, not transaction signing or private-key handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet lookup activity can reveal public wallet addresses and timing to PancakeSwap Explorer, public RPC providers, token or price APIs, and npm-installed SDK dependencies. <br>
Mitigation: Use only public wallet addresses, avoid the workflow when lookup privacy is a concern, and prefer trusted network and package-install environments. <br>
Risk: Deep links and optional browser-opening behavior can lead users into an external PancakeSwap UI where transactions are reviewed and confirmed. <br>
Mitigation: Open only PancakeSwap finance URLs, review all wallet prompts before confirming, and do not provide seed phrases or private keys. <br>


## Reference(s): <br>
- [Collect Fees on ClawHub](https://clawhub.ai/pcs-bot/pcs-collect-fees) <br>
- [PancakeSwap AI GitHub homepage](https://github.com/pancakeswap/pancakeswap-ai) <br>
- [fetch-v3-positions.mjs](references/fetch-v3-positions.mjs) <br>
- [fetch-infinity-positions.mjs](references/fetch-infinity-positions.mjs) <br>
- [fetch-solana.cjs](references/fetch-solana.cjs) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, JSON, Guidance] <br>
**Output Format:** [Markdown fee summaries with tables, shell command snippets, helper-script JSON, and PancakeSwap deep links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only workflow; helper scripts query public chain, explorer, token, and price endpoints and do not request signing material.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
