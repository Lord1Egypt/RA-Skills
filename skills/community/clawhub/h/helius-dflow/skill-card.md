## Description: <br>
Build Solana trading applications combining DFlow trading APIs with Helius infrastructure, including spot swaps, prediction markets, real-time market streaming, Proof KYC, transaction submission via Sender, fee optimization, LaserStream, and wallet intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xIchigo](https://clawhub.ai/user/0xIchigo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build Solana trading, prediction-market, wallet-intelligence, and real-time streaming applications that combine DFlow trading APIs with Helius infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated trading code could sign or submit transactions before the user has reviewed amounts, tokens, slippage, fees, and spending limits. <br>
Mitigation: Require explicit user approval before signing or submitting transactions, and surface amounts, token mints, slippage, fees, and spend limits in the application workflow. <br>
Risk: API keys, JWTs, or keypair files used by Helius, DFlow, or local tooling could be exposed in source code, logs, or shared configuration. <br>
Mitigation: Use project-scoped installation where possible, store credentials in environment variables or approved secret stores, and never embed private keys or API keys in code or logs. <br>
Risk: Prediction-market features may require KYC, geoblocking, market-status checks, and maintenance-window handling. <br>
Mitigation: Gate prediction-market trades with Proof KYC and jurisdiction checks, confirm market status before ordering, and avoid order submission during documented maintenance windows. <br>
Risk: Production use of DFlow dev endpoints, raw browser calls, or unverified MCP packages can cause reliability, CORS, rate-limit, or supply-chain issues. <br>
Mitigation: Verify external MCP packages before installation, use backend proxies for DFlow Trade API calls from web apps, and move production workloads to appropriate API keys and plan tiers. <br>


## Reference(s): <br>
- [DFlow Prediction Markets - Discovery, Trading & Redemption](references/dflow-prediction-markets.md) <br>
- [DFlow Proof KYC - Identity Verification](references/dflow-proof-kyc.md) <br>
- [DFlow Spot Trading - Token Swaps on Solana](references/dflow-spot-trading.md) <br>
- [DFlow WebSockets - Real-Time Market Data](references/dflow-websockets.md) <br>
- [DAS API - Digital Asset Standard](references/helius-das.md) <br>
- [LaserStream - High-Performance gRPC Streaming](references/helius-laserstream.md) <br>
- [Onboarding - Account Setup, API Keys & Plans](references/helius-onboarding.md) <br>
- [Priority Fees - Transaction Landing Optimization](references/helius-priority-fees.md) <br>
- [Helius Sender - Transaction Submission](references/helius-sender.md) <br>
- [Wallet API - Wallet Intelligence & Investigation](references/helius-wallet-api.md) <br>
- [WebSockets - Real-Time Solana Streaming](references/helius-websockets.md) <br>
- [Integration Patterns - Helius x DFlow](references/integration-patterns.md) <br>
- [Helius Docs](https://www.helius.dev/docs) <br>
- [Helius LLM-Optimized Docs](https://www.helius.dev/docs/llms.txt) <br>
- [DFlow MCP Server](https://pond.dflow.net/mcp) <br>
- [DFlow API Key](https://pond.dflow.net/build/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, configuration snippets, and API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Helius MCP tools, DFlow MCP tooling, REST APIs, WebSocket APIs, and local reference files depending on the user's task.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
