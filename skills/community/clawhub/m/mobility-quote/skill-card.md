## Description:

Get mobility route options worldwide, including fare estimates, ETA, and deeplinks to open supported ride apps through the KLO Mobility A2A agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ubunyod574-max](https://clawhub.ai/user/ubunyod574-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to compare available route options between two coordinates or places, including estimated price, ETA, and launcher links. It supports quote and discovery workflows, not guaranteed booking or payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trip origins and destinations are sent to the configured KLO Mobility endpoint.

Mitigation: Install and use only when sharing route coordinates with that third-party endpoint is acceptable.

Risk: Returned prices, summaries, provider names, and deeplinks are third-party supplied.

Mitigation: Treat quotes as estimates unless marked otherwise and check deeplink destinations before opening ride links.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ubunyod574-max/skills/mobility-quote)
- [A2A Registry Entry](https://a2aregistry.org/?agent=80386a0c-03c9-4bde-b93a-f9e6082937cd)
- [Publisher Profile](https://clawhub.ai/user/ubunyod574-max)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with A2A JSON-RPC request examples and structured quote fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the example call; responses may include estimated prices, ETAs, provider names, and third-party deeplinks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
