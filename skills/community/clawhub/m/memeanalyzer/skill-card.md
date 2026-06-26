## Description: <br>
Analyzes Solana meme token contract addresses for holder concentration, suspected insider wallets, and token risk signals using DexScreener and Solana RPC data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ultranumblol](https://clawhub.ai/user/ultranumblol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agents use this skill to assess Solana meme token contract addresses for concentration, suspected insider wallet patterns, and rug-risk indicators before acting on a token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted API path can initiate wallet-based USDC payments through x402. <br>
Mitigation: Prefer the local Python script unless paid API use is explicitly approved; set a spending limit and approve each paid request. <br>
Risk: The analyzer depends on external Solana RPC and DexScreener lookups, so results may be unavailable, delayed, or incomplete. <br>
Mitigation: Use a Helius API key for more reliable local RPC access and treat the output as one input to token review rather than a final trading decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ultranumblol/memeanalyzer) <br>
- [Helius RPC](https://helius.xyz/) <br>
- [Hosted analysis API](https://solana-meme-analyzer-production.up.railway.app/analyze?ca=TOKEN_CA) <br>
- [x402 facilitator](https://x402.org/facilitator) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, json, text, shell commands, guidance] <br>
**Output Format:** [Terminal text and optional JSON risk report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Solana token contract address; HELIUS_API_KEY improves reliability for local analysis, and the hosted API path may require wallet-based USDC payment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
