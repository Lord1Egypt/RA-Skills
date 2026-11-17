## Description:

Build Solana applications with Helius infrastructure. Covers transaction sending (Sender), asset/NFT queries (DAS API), real-time streaming (WebSockets, Laserstream), event pipelines (webhooks), priority fees, wallet analysis, and agent onboarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xichigo](https://clawhub.ai/user/0xichigo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Solana applications with Helius infrastructure, including transaction submission, asset and wallet queries, real-time streaming, webhooks, priority fee handling, and account onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide payments, plan upgrades, renewals, tips, and transaction signing in Solana wallet workflows.

Mitigation: Require explicit user confirmation before payments, upgrades, renewals, tips, or transaction signing, and keep signup wallets funded only at the minimum needed balance.

Risk: The skill handles API keys, JWTs, and keypair files that could expose Helius accounts or wallets if mishandled.

Mitigation: Store credentials outside source control, prefer environment variables or secure MCP configuration, and rotate exposed API keys, JWTs, or keypairs.

Risk: The install and setup flow references mutable npm packages using latest tags.

Mitigation: Pin and verify Helius MCP and CLI package versions before installing in wallet, production, or billing contexts.

Risk: Webhook and streaming guidance can expose endpoints or event data if receivers are weakly protected.

Mitigation: Use HTTPS endpoints, authenticate webhook receivers, and review event payload handling before deployment.

## Reference(s):

- [DAS API - Digital Asset Standard](references/das.md)
- [Enhanced Transactions - Human-Readable Transaction Data](references/enhanced-transactions.md)
- [LaserStream - High-Performance gRPC Streaming](references/laserstream.md)
- [Onboarding - Account Setup, API Keys & Plans](references/onboarding.md)
- [Priority Fees - Transaction Landing Optimization](references/priority-fees.md)
- [Helius Sender - Transaction Submission](references/sender.md)
- [Wallet API - Wallet Intelligence & Investigation](references/wallet-api.md)
- [Webhooks - Event-Driven Solana Notifications](references/webhooks.md)
- [WebSockets - Real-Time Solana Streaming](references/websockets.md)
- [Helius dashboard](https://dashboard.helius.dev)
- [Orb explorer](https://orbmarkets.io)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline code, shell commands, API examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use live Helius MCP tools when available; generated guidance can involve API keys, wallet payments, webhooks, and transaction submission.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
