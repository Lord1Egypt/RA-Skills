## Description:

A Polymarket trading CLI agent for researching markets, checking balances and positions, and placing buy or sell orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanswuhan](https://clawhub.ai/user/hanswuhan)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Polymarket markets and manage trades from a command-line agent with a Polygon wallet. It is intended for users who understand prediction-market, private-key, and live-trading risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a funded wallet private key.

Mitigation: Use a dedicated low-balance trading wallet, keep keys in local environment variables or a secret manager, and never paste private keys into chats or shared terminals.

Risk: The skill can place live buy and sell orders without adequate safeguards.

Mitigation: Require explicit trade confirmation or dry-run behavior before order submission and verify balance, token ID, side, price, and size before trading.

Risk: Runtime output may expose part of the private key.

Mitigation: Remove private-key prefix logging before use and avoid shared terminal sessions when running authenticated commands.

Risk: Unpinned dependencies can change trading behavior or security posture over time.

Mitigation: Use pinned, reviewed dependency versions and update only after testing the Polymarket client and wallet flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanswuhan/skills/polymarket-trade-agent)
- [Publisher profile](https://clawhub.ai/user/hanswuhan)
- [Polymarket](https://polymarket.com)
- [Polymarket CLOB API endpoint](https://clob.polymarket.com)
- [Polymarket Data API endpoint](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute authenticated Polymarket actions when configured with a funded wallet private key.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
