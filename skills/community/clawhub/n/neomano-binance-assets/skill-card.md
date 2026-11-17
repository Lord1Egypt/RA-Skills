## Description:

Safe, read-only Binance balance viewer (Spot wallet) using Binance API keys with READ-ONLY permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elandivar](https://clawhub.ai/user/elandivar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check Binance Spot wallet assets and balances without placing trades, transfers, withdrawals, margin, or futures actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Binance API credentials can expose sensitive account balance information.

Mitigation: Use a Binance API key with read-only permissions, no trading or withdrawal permissions, and an IP allowlist where available.

Risk: Printed balances are sensitive financial information.

Mitigation: Avoid sharing command output or logs that contain account assets and balances.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elandivar/skills/neomano-binance-assets)
- [Binance Spot Account API endpoint](https://api.binance.com/api/v3/account)
- [Binance API base URL](https://api.binance.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; the script prints JSON balance data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BINANCE_API_KEY/BINANCE_API_SECRET environment variables; defaults to non-zero Spot balances and supports --all and --min filters.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
