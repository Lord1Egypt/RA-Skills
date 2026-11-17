## Description:

x402 pay-per-call API for Amazon product search, filtering, ranking, detailed extraction, and one-shot "best products" recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hashcatter](https://clawhub.ai/user/hashcatter)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to query structured Amazon product intelligence, compare products, and build shopping recommendation workflows through the HashCats API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-initiated USDC micropayments may spend funds unexpectedly if wallet policy is too permissive.

Mitigation: Use strict per-call and session spend limits, prefer testnet unless intentionally enabling mainnet, and require confirmation for unexpected amounts, recipients, chains, or repeated paid calls.

## Reference(s):

- [HashCats API Homepage](https://api.hashcats.io)
- [HashCats API Docs](https://api.hashcats.io/docs)
- [HashCats OpenAPI](https://api.hashcats.io/openapi.json)
- [ClawHub Skill Page](https://clawhub.ai/hashcatter/skills/hashcats-amazon)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON API responses with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires x402 payment handling for paid API calls.]

## Skill Version(s):

0.1.0 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
