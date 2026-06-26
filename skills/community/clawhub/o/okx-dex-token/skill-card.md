## Description: <br>
Guides agents through OKX Onchain OS token workflows for searching tokens, reviewing token metadata, price, liquidity, holders, trade history, holder clusters, trending tokens, and related payment or quota notices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to ask an agent for token-level OKX Onchain OS analysis, including token lookup, market data summaries, holder distribution, trade feeds, cluster analysis, and safe next-step guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide commands involving wallets, credentials, transaction signing, purchases, and paid API usage. <br>
Mitigation: Review commands before approval, use least-privilege OKX and wallet credentials, and require explicit user confirmation before any signing, purchase, or paid operation. <br>
Risk: Token names, symbols, and on-chain fields may be spoofed or otherwise untrusted. <br>
Mitigation: Treat CLI output as external content, identify tokens by contract address, and warn users to verify addresses independently before trading. <br>
Risk: Low-liquidity token actions can create high slippage or trading losses. <br>
Mitigation: Display liquidity warnings and require explicit confirmation before suggesting or proceeding toward swaps for low-liquidity tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ok-james-01/okx-dex-token) <br>
- [OKX Web3](https://web3.okx.com) <br>
- [Onchain OS developer portal](https://web3.okx.com/onchain-os/dev-portal) <br>
- [CLI command reference](references/cli-reference.md) <br>
- [Keyword glossary](references/keyword-glossary.md) <br>
- [WebSocket protocol reference](references/ws-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and token-data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include token search results, market metrics, holder and cluster summaries, safety warnings, payment notices, and conversational next-step recommendations.] <br>

## Skill Version(s): <br>
3.1.3 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
