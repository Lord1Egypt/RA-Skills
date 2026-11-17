## Description:

Polymarket API and data access guide. Learn how to connect, find markets, get real-time data via WebSocket, access order books, place orders via CLOB SDK, and understand market mechanics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nwcalvin](https://clawhub.ai/user/nwcalvin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect agents or applications to Polymarket market data, WebSocket streams, order books, and CLOB SDK trading flows. It is most useful for building prediction-market data tools or carefully reviewed trading integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide or run live Polymarket trading code that places real orders.

Mitigation: Require human confirmation or dry-run behavior before placing orders, and review order size, price, side, token ID, and market before execution.

Risk: The trading helper handles wallet private keys and derives API credentials.

Mitigation: Use a dedicated low-balance wallet, avoid primary private keys, and keep credentials out of shared logs, prompts, and committed files.

Risk: Dependencies such as py-clob-client can affect wallet signing and order submission behavior.

Mitigation: Pin, review, and update dependencies deliberately before deploying the skill in an agent environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nwcalvin/skills/innotech-polymarket-api)
- [Polymarket API Reference](references/API_REFERENCE.md)
- [Polymarket WebSocket Guide](references/WEBSOCKET_GUIDE.md)
- [Polymarket Create Orders Documentation](https://docs.polymarket.com/trading/orders/create)
- [Polymarket Orders Overview](https://docs.polymarket.com/trading/orders/overview)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide live API calls, WebSocket subscriptions, and CLOB order placement when the user provides credentials and executes the examples.]

## Skill Version(s):

2.0.0 (source: evidence.release.version, artifact/skill.json, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
