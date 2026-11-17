## Description:

Crypto APIs (cryptoapis.io). Use this skill for ANY Crypto APIs request — searching and reading data. Whenever a task involves Crypto APIs, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read Crypto APIs market data through an OOMOL-connected account, including asset details, exchange rates, and supported assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run downloaded code and introduce persistent agent changes without clear approval.

Mitigation: Prefer an existing trusted oo CLI installation; review and verify any installer before execution; explicitly approve persistent changes. Set OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill synchronization.

## Reference(s):

- [Crypto APIs homepage](https://cryptoapis.io)
- [Crypto APIs API documentation](https://developers.cryptoapis.io/v-2.2024-12-12-175/RESTapis/general-information/overview)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Crypto APIs ClawHub release](https://clawhub.ai/oomol/skills/oo-crypto-apis)

## Skill Output:

**Output Type(s):** [API data, Text, JSON]

**Output Format:** [JSON market data returned for the requested lookup, with natural-language guidance from the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only asset, exchange-rate, and supported-asset lookups; requires an established OOMOL connection.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
