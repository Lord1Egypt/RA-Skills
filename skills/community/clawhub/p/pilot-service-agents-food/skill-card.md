## Description:

Food, recipes, and nutrition lookups through Pilot Protocol service agents for OpenFoodFacts, TheCocktailDB, TheMealDB, Fruityvice, and Open Brewery DB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and external users use this skill to discover and query Pilot Protocol food service agents for packaged-food lookups, recipe searches, ingredient data, brewery searches, and reference nutrition data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Nutrition and recipe data may be incomplete or unsuitable for medical decisions.

Mitigation: Treat returned nutrition and recipe data as reference information only, and route medical nutrition advice or calorie-tracking needs to an appropriate health workflow.

Risk: Summary requests may return Gemini-generated prose through the service-agent workflow.

Mitigation: Prefer structured /data responses for factual extraction and review generated summaries before relying on them.

Risk: Results depend on Pilot Protocol daemon, overlay network, directory-agent availability, and upstream community-maintained catalogs.

Mitigation: Verify the agent contract with /help or a fresh list-agents query, handle unavailable or truncated responses, and inspect upstream_url when present.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-food)
- [Pilot Skills Index](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Service-agent responses may include JSON data envelopes, plain-text help, or Gemini-generated prose summaries.]

## Skill Version(s):

1.0.0 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
