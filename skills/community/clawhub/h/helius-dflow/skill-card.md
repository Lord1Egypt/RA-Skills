## Description:

Build Solana trading applications combining DFlow trading APIs with Helius infrastructure, including spot swaps, prediction markets, real-time streaming, Proof KYC, transaction submission, fee optimization, LaserStream, and wallet intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xichigo](https://clawhub.ai/user/0xichigo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Solana trading applications that combine DFlow trading APIs with Helius infrastructure for swaps, prediction-market workflows, streaming, transaction submission, fee estimation, and wallet or asset intelligence.

### Deployment Geography for Use:

Global, subject to jurisdictional restrictions for prediction-market trading.

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable external MCP tooling.

Mitigation: Use a pinned, trusted Helius MCP version and restrict the server's filesystem and network access before installing.

Risk: Trading, signup, renewal, upgrade, and transaction-signing flows may involve real funds or account changes.

Mitigation: Require explicit human approval before any payment, account-plan change, or transaction signing.

Risk: Wallet keys, JWTs, API keys, or KYC data could be exposed if handled on shared machines or in client-side code.

Mitigation: Keep secrets in environment variables or backend secret storage, avoid shared machines for sensitive wallet material, and use backend handling for API keys and KYC flows.

Risk: Generated transaction instructions can be incorrect or unsafe for a user's intent.

Mitigation: Validate DFlow transaction instructions, amounts, mints, market status, KYC status, and fees before signing.

## Reference(s):

- [DFlow Spot Trading](references/dflow-spot-trading.md)
- [DFlow Prediction Markets](references/dflow-prediction-markets.md)
- [DFlow Proof KYC](references/dflow-proof-kyc.md)
- [DFlow WebSockets](references/dflow-websockets.md)
- [Helius Sender](references/helius-sender.md)
- [Helius Priority Fees](references/helius-priority-fees.md)
- [Helius WebSockets](references/helius-websockets.md)
- [Helius LaserStream](references/helius-laserstream.md)
- [Helius DAS API](references/helius-das.md)
- [Helius Wallet API](references/helius-wallet-api.md)
- [Helius Onboarding](references/helius-onboarding.md)
- [Integration Patterns](references/integration-patterns.md)
- [Helius Docs](https://www.helius.dev/docs)
- [Helius API Reference](https://www.helius.dev/docs/api-reference)
- [Helius LLM-Optimized Docs](https://www.helius.dev/docs/llms.txt)
- [DFlow Docs](https://pond.dflow.net/introduction)
- [DFlow MCP Docs](https://pond.dflow.net/build/mcp)
- [DFlow Cookbook](https://github.com/DFlowProtocol/cookbook)
- [DFlow Proof Docs](https://pond.dflow.net/learn/proof)
- [Helius LaserStream SDK](https://github.com/helius-labs/laserstream-sdk)
- [ClawHub Skill Page](https://clawhub.ai/0xichigo/skills/helius-dflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose API calls, MCP server setup, environment variables, transaction-handling patterns, and implementation guidance for Solana trading applications.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
