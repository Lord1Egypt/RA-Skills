## Description:

Pay HTTP 402 payment challenges using tokens via the Tempo CLI and Uniswap Trading API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to complete paid API calls after HTTP 402 challenges, including MPP and x402 flows, by preparing Tempo CLI payments and Uniswap Trading API swap or bridge steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide real crypto payments, swaps, approvals, bridges, and signatures using wallet authority.

Mitigation: Use a dedicated low-balance wallet and verify every amount, token, recipient, chain, and gas estimate before signing or broadcasting.

Risk: Private keys and API keys can be exposed through shell history, environment handling, or copied commands.

Mitigation: Avoid production private keys, never hardcode or commit secrets, and prefer short-lived or isolated credentials for payment testing.

Risk: Automatic payment and autoSwap examples can spend funds if an endpoint, price, or challenge is not trusted.

Mitigation: Prefer dry-run and manual confirmation flows, require explicit approval at each signing or transaction gate, and set strict spending limits.

Risk: Bridge or payment recipient mistakes can send funds to the wrong wallet.

Mitigation: Confirm that bridge destinations use the Tempo wallet address when funding Tempo, not the source ERC-20 wallet, before broadcasting.

## Reference(s):

- [Credential Construction](references/credential-construction.md)
- [Trading API Flows](references/trading-api-flows.md)
- [Tempo CLI](https://tempo.xyz)
- [Tempo Documentation](https://mainnet.docs.tempo.xyz)
- [Machine Payment Protocol](https://mpp.dev)
- [MPP Services Catalog](https://mpp.dev/api/services)
- [Uniswap Developers](https://developers.uniswap.org/)
- [Uniswap Trading API](https://trade-api.gateway.uniswap.org/v1)
- [x402 Specification](https://github.com/coinbase/x402)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include transaction, approval, signing, swap, bridge, and retry steps that require user confirmation before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
