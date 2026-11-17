## Description:

Set up automated trading on Polymarket, including wallet setup, token approvals, API authentication, market discovery, order placement, WebSocket feeds, and position management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emsin44](https://clawhub.ai/user/emsin44)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to configure and validate automated Polymarket trading workflows, including credentials, approvals, API connectivity, order placement, and position tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real wallet private keys and Polymarket API credentials.

Mitigation: Use a dedicated low-balance wallet, store secrets in a secret manager or encrypted environment, and never commit credentials.

Risk: The skill can guide token approvals and live order submission with real funds.

Mitigation: Require explicit user approval before token approvals or live orders, and prefer bounded approval amounts matched to expected trading volume.

Risk: Unpinned or drifting dependencies can change trading behavior.

Mitigation: Pin and lock dependencies before running the setup in an automated trading environment.

## Reference(s):

- [Polymarket Trading API Guide](artifact/GUIDE.md)
- [ClawHub Skill Page](https://clawhub.ai/emsin44/skills/polymarket-setup)
- [py-clob-client](https://github.com/Polymarket/py-clob-client)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)
- [Polymarket Data API](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, JSON examples, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose live trading setup steps that require wallet keys, API credentials, token approvals, and explicit user approval before order submission.]

## Skill Version(s):

1.0.6 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
