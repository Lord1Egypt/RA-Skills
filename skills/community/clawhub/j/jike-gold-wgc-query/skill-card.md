## Description:

Queries latest and historical World Gold Council gold prices through Jike API, with optional date, weight-unit, and currency filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current or historical international gold-price data and present price date, update time, weight unit, currency, and price. Returned market data should be treated as informational and not as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An undocumented API-base override can redirect the Jike AppKey to an arbitrary endpoint.

Mitigation: Keep JIKE_API_BASE_URL unset or locked to https://api.jikeapi.cn, use a low-privilege API key, and rotate the key if it may have run with an untrusted base URL.

Risk: Gold-price data can be mistaken for investment advice.

Mitigation: Use the skill only for explicit live or historical price lookups and preserve the informational, non-investment-advice framing in responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-gold-wgc-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike WGC latest gold price endpoint](https://api.jikeapi.cn/v1/gold/wgc/latest)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text tables or JSON returned by a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JIKE_GOLD_WGC_QUERY_KEY or JIKE_APPKEY credential. The script can query latest prices or historical prices filtered by date, weight unit, and currency.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
