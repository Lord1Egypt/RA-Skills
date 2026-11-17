## Description:

Queries Polymarket prediction markets for market prices, event probabilities, betting odds, and related Polymarket data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyshmueli](https://clawhub.ai/user/dannyshmueli)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query public Polymarket market and event data, including prices, probabilities, volume, liquidity, and market status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to Polymarket's public API for market data.

Mitigation: Review network permissions and disclose the public API dependency before installing or running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dannyshmueli/skills/pm-odds)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Plain text summaries or raw JSON from command-line execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market summaries include question, outcome prices, 24-hour volume, total volume, liquidity, status, and optional descriptions when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
