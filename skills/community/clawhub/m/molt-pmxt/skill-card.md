## Description:

Grants the agent real-time access to prediction markets (Polymarket, Kalshi, Limitless) for fact-checking, probability analysis, and order execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realfishsam](https://clawhub.ai/user/realfishsam)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent search prediction markets, retrieve market-implied probabilities, compare prices across exchanges, and execute prediction-market orders when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live prediction-market orders using configured private keys or API credentials.

Mitigation: Use dedicated low-balance accounts, least-privilege or revocable credentials, explicit exchange selection, and external spending or confirmation controls before enabling order execution.

Risk: Runtime credentials for Polymarket, Kalshi, and Limitless can authorize account access or order signing.

Mitigation: Store credentials only in the agent runtime secret manager, rotate or revoke them when no longer needed, and avoid exposing private keys in prompts, logs, or shared files.

Risk: Market-implied probabilities can be mistaken for verified facts or financial advice.

Mitigation: Present outputs as market pricing signals, cite the relevant market context, and require human review before acting on trading or hedging recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/realfishsam/skills/molt-pmxt)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown text with structured market data, probability quotes, and order status objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require exchange credentials and can initiate live prediction-market orders when explicitly invoked.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
