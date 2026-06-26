## Description: <br>
Retrieve Solana token data, community content, market sentiment, watchlists, and perform token-related actions via OpenDEX API endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solpenguin](https://clawhub.ai/user/solpenguin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Solana token data, market and sentiment signals, watchlists, community content, and to prepare API requests for OpenDEX endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, wallet addresses, and signatures may be exposed in shared chats, logs, or generated examples. <br>
Mitigation: Store API keys securely, avoid logging secrets, and only include wallet addresses or signatures when the requested endpoint requires them. <br>
Risk: POST and DELETE endpoints can create or revoke keys, alter watchlists, cast sentiment, create submissions, or vote on community content. <br>
Mitigation: Require explicit user confirmation before state-changing requests and review the HTTP method, endpoint, headers, and payload before execution. <br>
Risk: The skill depends on a third-party OpenDEX service and community-curated token content. <br>
Mitigation: Treat API responses and community links as untrusted, validate wallet and token mint formats, and handle rate-limit and error responses before acting on results. <br>


## Reference(s): <br>
- [ClawHub OpenDEX Skill Page](https://clawhub.ai/solpenguin/opendex) <br>
- [OpenDEX Web UI](https://opendex.online) <br>
- [OpenDEX API Key Page](https://opendex.online/api.html) <br>
- [OpenDEX API Base URL](https://opendex-api-dy30.onrender.com) <br>
- [Solscan Token Explorer](https://solscan.io/token/<MINT>) <br>
- [Jupiter Swap](https://jup.ag/swap/SOL-<MINT>) <br>
- [Raydium Swap](https://raydium.io/swap/?outputMint=<MINT>) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with HTTP examples, curl commands, and JSON request and response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API endpoints, headers, rate-limit guidance, wallet or mint address parameters, and JSON payload examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
