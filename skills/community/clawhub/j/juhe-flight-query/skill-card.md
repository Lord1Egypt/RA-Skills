## Description:

Queries domestic flight options through the Juhe API using departure airport, arrival airport, and travel date, returning flight numbers, times, ticket prices, airline names, and transfer details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to look up flight options by route and departure date, especially for China domestic routes available through Juhe. The skill helps an agent guide setup, convert city requests to airport codes, run the provided Python query script, and present flight results clearly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight search details are sent to Juhe when the skill queries live flight data.

Mitigation: Use the skill only when sharing the route and departure date with Juhe is acceptable.

Risk: The Juhe API key can be exposed if passed on the command line, committed in scripts/.env, or captured in logs.

Mitigation: Set JUHE_FLIGHT_KEY through the environment or a managed secret store, avoid command-line key arguments, do not commit scripts/.env, and rotate any exposed key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-flight-query)
- [Publisher profile](https://clawhub.ai/user/juhemcp)
- [Juhe Flight Query API documentation](https://www.juhe.cn/docs/api/id/818)
- [Juhe data service platform](https://www.juhe.cn)
- [Juhe flight query endpoint](https://apis.juhe.cn/flight/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown setup guidance and plain text flight query results, with the script also printing JSON API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JUHE_FLIGHT_KEY; sends route and departure date query parameters to apis.juhe.cn.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
