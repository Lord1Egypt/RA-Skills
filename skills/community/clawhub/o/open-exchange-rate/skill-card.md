## Description:

Get real-time exchange rates and currency conversion using free public ExchangeRate-API. No API key required. Use when users ask for current exchange rates, currency conversion calculations, or need to check currency prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alone86136](https://clawhub.ai/user/alone86136)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to retrieve current exchange rates, convert amounts between currencies, and list supported currency codes through simple Python scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound HTTPS requests to open.er-api.com when a user asks for rates, conversions, or currency lists.

Mitigation: Use it only in environments where that endpoint is allowed, or review and allowlist the endpoint before deployment.

Risk: Rate and currency results depend on the availability and freshness of the public currency API.

Mitigation: Check the returned last-updated timestamp before relying on results for time-sensitive decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alone86136/skills/open-exchange-rate)
- [ExchangeRate-API public endpoint](https://open.er-api.com/v6/latest/USD)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text command output with exchange-rate tables, conversion summaries, or currency-code lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires outbound HTTPS access to open.er-api.com when invoked; no API key is required.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
