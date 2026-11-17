## Description:

Build frontend Solana applications with Phantom Connect SDK and Helius infrastructure. Covers React, React Native, and browser SDK integration, transaction signing via Helius Sender, API key proxying, token gating, NFT minting, crypto payments, real-time updates, and secure frontend architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xichigo](https://clawhub.ai/user/0xichigo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Solana web and mobile applications that connect Phantom wallets, proxy Helius APIs, submit and verify transactions, query wallet and asset data, and implement token gating, NFT minting, payments, and real-time updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-capable and transaction-signing workflows can spend funds if applied without explicit user consent.

Mitigation: Require clear user confirmation before signup, upgrades, renewals, wallet auto-confirm, or any transaction that spends funds.

Risk: Helius API keys, JWTs, and wallet-related secrets may be exposed if placed in browser bundles or loosely stored.

Mitigation: Keep secrets in restricted server-side storage and route non-browser-safe Helius calls through authenticated backend proxies.

Risk: Proxy, payment-verification, token-gating, and SSE examples are starting points and may be under-scoped for production.

Mitigation: Harden examples with authentication, allowlists, schema validation, durable rate limits, nonce-based signing, exact payment verification, replay protection, and user-facing disclosure.

Risk: Install guidance uses mutable package versions such as @latest.

Mitigation: Pin MCP and starter package versions before installation or production reuse.

## Reference(s):

- [Browser SDK Reference](references/browser-sdk.md)
- [Frontend Security](references/frontend-security.md)
- [DAS API](references/helius-das.md)
- [Enhanced Transactions](references/helius-enhanced-transactions.md)
- [Helius Onboarding](references/helius-onboarding.md)
- [Priority Fees](references/helius-priority-fees.md)
- [Helius Sender](references/helius-sender.md)
- [Helius Wallet API](references/helius-wallet-api.md)
- [Helius WebSockets](references/helius-websockets.md)
- [Integration Patterns](references/integration-patterns.md)
- [NFT Minting](references/nft-minting.md)
- [Crypto Payments](references/payments.md)
- [React Native SDK Reference](references/react-native-sdk.md)
- [React SDK Reference](references/react-sdk.md)
- [Token-Gated Access](references/token-gating.md)
- [Transaction Patterns Reference](references/transactions.md)
- [Phantom Developer Docs](https://docs.phantom.com)
- [Phantom Portal](https://phantom.com/portal)
- [Helius Docs](https://www.helius.dev/docs)
- [Helius API Reference](https://www.helius.dev/docs/api-reference)
- [Helius Rate Limits](https://www.helius.dev/docs/billing/rate-limits.md)
- [Phantom React SDK](https://www.npmjs.com/package/@phantom/react-sdk)
- [Phantom Browser SDK](https://www.npmjs.com/package/@phantom/browser-sdk)
- [Phantom React Native SDK](https://www.npmjs.com/package/@phantom/react-native-sdk)
- [Solana Kit](https://www.npmjs.com/package/@solana/kit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose frontend, backend proxy, wallet integration, transaction, and MCP setup patterns; user review is required before executing generated commands or fund-moving transactions.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
