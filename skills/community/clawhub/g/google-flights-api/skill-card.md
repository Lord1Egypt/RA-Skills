## Description:

Search Google Flights for a route and date as structured JSON, including price, airline, duration, stops, and legs for round-trip, one-way, and multi-city itineraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to search flight routes, compare fares, carriers, durations, stops, and plan round-trip, one-way, or multi-city itineraries through Scavio's Google Flights API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight search details and the Scavio API key are sent to Scavio.

Mitigation: Tell users about the external API call and keep SCAVIO_API_KEY in an environment variable or secret store.

Risk: Each successful request costs one Scavio credit.

Mitigation: Confirm the user is ready to spend credits before making searches that may require multiple requests.

Risk: Returned fares, airlines, times, and durations may be misrepresented if the agent fabricates or transforms results without grounding.

Mitigation: Return only API-provided flight data and state the requested currency when quoting fares.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scavio-ai/skills/google-flights-api)
- [Scavio Google Flights API Documentation](https://scavio.dev/docs/google-flights?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-flights-api)
- [Scavio Rate Limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-flights-api)

## Skill Output:

**Output Type(s):** [JSON, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with API request examples and structured JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; each successful Google Flights request uses one Scavio credit.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
