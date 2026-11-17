## Description:

Fetches and summarizes a multichain EVM wallet portfolio through heyAura's paid x402 API, including token balances, USD values, networks, and DeFi positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyaura](https://clawhub.ai/user/heyaura)

### License/Terms of Use:

MIT-0

## Use Case:

Wallet holders and developers use this skill to inspect an EVM address or ENS name and summarize its holdings, values by chain, and DeFi positions. Paid requests require explicit authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid requests can spend funds using a local EVM payer key.

Mitigation: Use a dedicated, limited-funds wallet; inspect live payment terms and obtain explicit authorization before paying.

Risk: An uncertain settlement or expired payment identifier can lead to another charge on retry.

Mitigation: Do not retry paid requests automatically; confirm settlement and seek authorization before a retry.

Risk: Portfolio details are saved to a local temporary JSON file.

Mitigation: Handle the file as sensitive financial data and remove it when no longer needed.

## Reference(s):

- [heyAura portfolio API reference](references/portfolio-api.md)
- [heyAura OpenAPI specification](https://aura.adex.network/.well-known/openapi.json)
- [heyAura skill on ClawHub](https://clawhub.ai/heyaura/skills/heyaura)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Portfolio summary in Markdown; full API response in a local temporary JSON file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-network balances, USD values, and DeFi positions when available.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
