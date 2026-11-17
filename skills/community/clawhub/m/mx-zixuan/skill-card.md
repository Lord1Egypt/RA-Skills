## Description:

Manages a user's Eastmoney A-share self-selected stock watchlist by querying, adding, or deleting entries only when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoeluli7459-dev](https://clawhub.ai/user/zoeluli7459-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to query or update a personal Eastmoney self-selected A-share watchlist from an agent session when they provide clear query, add, or delete intent and, for mutations, a stock name or six-digit code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated add and delete operations can change the user's personal Eastmoney watchlist.

Mitigation: Use only explicit query, add, or delete requests, and require a clear stock name or six-digit code before mutating the list.

Risk: The skill requires an Eastmoney API key and may read MX_APIKEY from an environment variable or parent .env file.

Mitigation: Install only when the user is comfortable granting watchlist access, and store the API key in a controlled local environment.

Risk: The security evidence notes possible over-reporting of mutation success on inconsistent API responses.

Mitigation: Report API messages accurately and query the watchlist after a mutation when the user needs confirmation.

## Reference(s):

- [A股自选股 ClawHub Skill Page](https://clawhub.ai/zoeluli7459-dev/skills/mx-zixuan)
- [mx-zixuan Result Fields](references/result-fields.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Text summaries with generated CSV and JSON files for watchlist queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY; query results may include stock code, name, latest price, change, turnover rate, and volume ratio.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
