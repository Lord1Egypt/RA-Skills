## Description: <br>
Build Solana applications with Helius infrastructure. Covers transaction sending (Sender), asset/NFT queries (DAS API), real-time streaming (WebSockets, Laserstream), event pipelines (webhooks), priority fees, wallet analysis, and agent onboarding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xIchigo](https://clawhub.ai/user/0xIchigo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build Solana applications with Helius infrastructure, including transaction sending, asset queries, real-time monitoring, webhooks, wallet analysis, onboarding, billing, and troubleshooting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through workflows involving locally saved API keys, keypairs, and JWT files. <br>
Mitigation: Use environment variables or protected local storage, remove temporary key material after use, and avoid committing credentials to repositories. <br>
Risk: The skill can guide real crypto payments, account upgrades, renewals, token transfers, and transaction sending. <br>
Mitigation: Require explicit user approval for signup, billing, plan changes, token transfers, and transaction sends; test with a dedicated low-balance wallet. <br>
Risk: The evidence security verdict is suspicious because the skill can direct agents through sensitive crypto and account-management actions. <br>
Mitigation: Install only if the Helius MCP package and publisher are trusted, prefer a pinned MCP version, and review generated actions before execution. <br>


## Reference(s): <br>
- [DAS API - Digital Asset Standard](references/das.md) <br>
- [Enhanced Transactions - Human-Readable Transaction Data](references/enhanced-transactions.md) <br>
- [LaserStream - High-Performance gRPC Streaming](references/laserstream.md) <br>
- [Onboarding - Account Setup, API Keys & Plans](references/onboarding.md) <br>
- [Priority Fees - Transaction Landing Optimization](references/priority-fees.md) <br>
- [Helius Sender - Transaction Submission](references/sender.md) <br>
- [Wallet API - Wallet Intelligence & Investigation](references/wallet-api.md) <br>
- [Webhooks - Event-Driven Solana Notifications](references/webhooks.md) <br>
- [WebSockets - Real-Time Solana Streaming](references/websockets.md) <br>
- [ClawHub skill page](https://clawhub.ai/0xIchigo/helius) <br>
- [Helius dashboard](https://dashboard.helius.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks, commands, configuration steps, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to use Helius MCP tools and Helius APIs for live Solana data, account setup, transaction sending, streaming, webhooks, and wallet analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
