## Description:

Helps agents query pay-per-request crypto market, token screening, derivatives, and wallet data through x402 endpoints settled in USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perria080925-bot](https://clawhub.ai/user/perria080925-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and crypto researchers use this skill to request market indicators, examine DEX pairs and token risk flags, monitor funding and crowding, or summarize EVM wallet activity without a subscription or API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid requests, especially loops and watchlists, can accumulate USDC charges.

Mitigation: Confirm the expected number of calls and total cost with the user before payment or batch requests.

Risk: Wallet-address lookups can reveal sensitive activity or create privacy concerns.

Mitigation: Request consent from the address owner or confirm that the user accepts the privacy tradeoff before lookup.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/perria080925-bot/skills/odq-crypto-data)
- [Endpoint reference](references/endpoints.md)
- [x402 crypto data endpoints](https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain-text summaries of endpoint data, with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint data is informational, not financial advice; token safety scores are heuristic, not audits.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
