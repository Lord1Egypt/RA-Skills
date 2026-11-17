## Description:

Checks a Polymarket market's UMA settlement state on Polygon before a trade and returns an observe-only risk gate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[predge-ai](https://clawhub.ai/user/predge-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Trading agents and developers use this skill to check Polymarket settlement disputes, proposal windows, UMA votes and recent market updates before deciding whether to trade or reduce position size. It does not place orders or estimate trading edge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market identifiers are sent to Predge, and trade/skip decisions rely on its signed API output.

Mitigation: Share only identifiers you are comfortable disclosing and review the signed output before using it in a trading strategy.

Risk: An untrusted API override can redirect settlement checks to another endpoint.

Mitigation: Leave PREDGE_API_BASE unset unless you deliberately choose a trusted endpoint.

Risk: Optional Simmer market resolution uses an API key.

Mitigation: Provide SIMMER_API_KEY only when resolving Simmer market IDs; ordinary Polymarket checks need no key.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/predge-ai/skills/predge-settlement-risk)
- [Predge settlement-risk API example](https://api.predge.io/v1/settlement-risk/4424722)
- [Settlement-risk sample records](https://data.predge.io/samples/settlement-risk)
- [Predge public attestation keys](https://api.predge.io/.well-known/predge-keys.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable risk assessment and trade/skip decision, or JSON record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a risk level and position-size factor; no orders are placed.]

## Skill Version(s):

0.1.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
