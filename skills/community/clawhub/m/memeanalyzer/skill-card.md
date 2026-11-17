## Description:

Analyzes Solana token contract addresses for meme-token risk by checking holder distribution, suspected insider wallets, and top-holder concentration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ultranumblol](https://clawhub.ai/user/ultranumblol)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to assess Solana meme token risk before acting on a token contract address. It supports local script execution and a hosted pay-per-request API path for JSON-oriented agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags the hosted payment path as requiring review because it recommends wallet-based paid requests through mutable npm tooling.

Mitigation: Trust and pin the payment client before use, isolate wallet access, and confirm the 0.02 USDC x402 charge before authorizing payment.

Risk: Self-hosted payment configuration can depend on facilitator and recipient settings.

Mitigation: Validate FACILITATOR_URL and payment recipient configuration, and set only the environment variables needed for the selected deployment path.

Risk: The package includes PaxHeader archive metadata files.

Mitigation: Remove PaxHeader archive metadata from the release package before installation or redistribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ultranumblol/skills/memeanalyzer)
- [Helius](https://helius.xyz/)
- [Hosted x402 Analysis Endpoint](https://solana-meme-analyzer-production.up.railway.app/analyze?ca=TOKEN_CA)
- [Project Homepage Declared in Artifact Metadata](https://github.com/ultranumblol/solana-meme-analyzer)
- [Project Support Declared in Artifact Metadata](https://github.com/ultranumblol/solana-meme-analyzer/issues)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, API calls, guidance]

**Output Format:** [Console text tables and optional JSON; the hosted API returns JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Solana token contract address. A Helius API key improves local reliability, and the hosted API may require a 0.02 USDC x402 payment.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
