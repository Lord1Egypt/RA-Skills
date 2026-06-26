## Description: <br>
Execute Jupiter API operations on Solana, including fetching quotes, signing transactions, executing swaps, prediction markets, DCA, limit orders, lending, and related Jupiter integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifeofpavs](https://clawhub.ai/user/lifeofpavs) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to prepare Jupiter API requests and command-line workflows for Solana swaps, recurring orders, limit orders, lending, prediction markets, portfolio lookups, transaction signing, and transaction submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and broadcast Solana transactions that move real funds. <br>
Mitigation: Use a dedicated low-balance wallet and verify token mints, amounts, destinations, transaction payloads, and market details before signing or broadcasting. <br>
Risk: Wallet JSON files contain private key material. <br>
Mitigation: Avoid high-value wallets, keep wallet files local and protected, prefer ephemeral keys for testing, and use hardware signing where available. <br>
Risk: Autonomous execution could approve an incorrect swap, order, lending action, prediction-market trade, or claim transaction. <br>
Mitigation: Require human review before signing or sending transactions and avoid allowing the agent to autonomously sign or broadcast. <br>
Risk: The public Solana RPC endpoint is rate-limited and may be unreliable for production use. <br>
Mitigation: Configure a dedicated RPC provider through SOLANA_RPC_URL for production transaction submission. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lifeofpavs/jup-skill) <br>
- [Jupiter API Base URL](https://api.jup.ag) <br>
- [Jupiter Portal](https://portal.jup.ag) <br>
- [Jupiter Docs](https://dev.jup.ag) <br>
- [Jupiter LLM Docs](https://dev.jup.ag/llms.txt) <br>
- [Jupiter Full LLM Docs](https://dev.jup.ag/llms-full.txt) <br>
- [Solscan](https://solscan.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUP_API_KEY and, for signing, a local Solana wallet JSON file; SOLANA_RPC_URL is optional for transaction submission.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
