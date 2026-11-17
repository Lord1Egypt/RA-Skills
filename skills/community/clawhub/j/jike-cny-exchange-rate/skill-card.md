## Description:

This skill helps agents query RMB exchange-rate data from Jike Data, including supported currency lists, RMB foreign-exchange quotes, and currency conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill through an agent to list supported foreign currencies, look up RMB exchange-rate quotes, and convert amounts between currencies using Jike Data APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key-bearing requests can be redirected away from the stated provider if JIKE_API_BASE_URL is set.

Mitigation: Leave JIKE_API_BASE_URL unset unless the alternate endpoint is fully trusted and intended.

Risk: Currency, amount, and AppKey values are sent to the provider during lookups and conversions.

Mitigation: Use this skill only when that data sharing is acceptable, and store the AppKey in a protected environment variable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-cny-exchange-rate)
- [Jike Data homepage](https://www.jikeapi.cn/)
- [Jike CNY exchange-rate query endpoint](https://api.jikeapi.cn/v1/cny_exchange_rate/query)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text tables or JSON from a Python CLI, with shell commands for invocation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and an AppKey in JIKE_CNY_EXCHANGE_RATE_KEY or JIKE_APPKEY; sends currency, amount, and AppKey values to the configured API endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
