## Description:

Provides real-time and historical Indonesia Stock Exchange (IDX) market data through GoAPI for stock prices, issuer lists, market indexes, and company profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angween](https://clawhub.ai/user/angween)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up Indonesia Stock Exchange issuers, current or trending prices, historical end-of-day data, market indexes, and company profiles through GoAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full GoAPI request URLs can expose the GOAPI_KEY because the skill uses an api_key query parameter.

Mitigation: Do not paste full request URLs into chats, logs, screenshots, or bug reports; rotate the key if a URL containing it is exposed.

Risk: Market data requests may fail when the GOAPI_KEY is invalid or the account quota is exhausted.

Mitigation: Surface the server response clearly and ask the user to verify credentials or quota before retrying.

## Reference(s):

- [GoAPI](https://goapi.io)
- [ClawHub skill page](https://clawhub.ai/angween/skills/idx-market-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown tables or lists with IDX market data and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices are presented in Indonesian Rupiah (IDR) when available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
