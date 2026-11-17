## Description:

ClawPump V2 Token Launchpad helps agents launch real on-chain SPL tokens priced in CLAW through Meteora DBC, trade pools, and monitor graduation to DAMM v2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maliot100x](https://clawhub.ai/user/maliot100x)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to guide Solana token launches, swaps, pool-state checks, and wallet-signing flows for CLAW-quoted ClawPump v2 pools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may handle raw wallet keys or expose private keys during hosted-agent wallet flows.

Mitigation: Use a low-value wallet, avoid displaying or pasting private keys in chat, and prefer Phantom, Solflare, or a protected signer with explicit approval.

Risk: Server-built mainnet transactions may be signed without enough independent validation.

Mitigation: Validate each returned transaction, wallet address, token metadata, pool address, and expected fee impact before signing or broadcasting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maliot100x/skills/grok-implement)
- [ClawPump V2 homepage](https://clawpump-v2.vercel.app)

## Skill Output:

**Output Type(s):** [Guidance, Code, API calls, Configuration]

**Output Format:** [Markdown guidance with TypeScript, JSON, and HTTP endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HELIUS_RPC for headless agent RPC access; signing and transaction approval remain with the user or agent wallet.]

## Skill Version(s):

0.7.1 (source: server release metadata; artifact frontmatter lists 0.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
