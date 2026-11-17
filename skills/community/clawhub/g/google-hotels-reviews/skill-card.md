## Description:

Google Hotels review text is not available through StayingAPI; this skill directs agents to use Google Hotels aggregate ratings or review text from Booking.com, Airbnb, or Vrbo instead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent is asked for Google Hotels reviews, so the agent can explain that review text is unavailable and route the user to aggregate ratings or supported review platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live StayingAPI key may be stored or used for billable live hotel-data calls.

Mitigation: Use a sandbox stay_test_ key for evaluation, keep live keys scoped to StayingAPI, and review StayingAPI pricing before live use.

Risk: Users may expect Google Hotels review text even though the Google reviews endpoint is not enabled.

Mitigation: State that Google Hotels review text is unavailable through StayingAPI and offer aggregate ratings from /v1/search or review text from Booking.com, Airbnb, or Vrbo.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stayingapi/skills/google-hotels-reviews)
- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI docs](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI pricing](https://stayingapi.com/pricing)
- [Authentication setup](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline HTTP and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STAYINGAPI_KEY for API examples; live calls require internet access to api.stayingapi.com.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
