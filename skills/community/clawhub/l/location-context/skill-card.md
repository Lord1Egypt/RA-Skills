## Description:

Get comprehensive context about a location including nearby places, area description, and optional weather.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:


## Use Case:

Agents, developers, and external users use this skill to retrieve location-aware area summaries, nearby place context, tailored recommendations, and optional weather context for planning or recommendation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends location coordinates, radius, optional context, and weather options to Camino AI.

Mitigation: Avoid sending sensitive exact locations or private meeting details unless that disclosure is acceptable for the use case.

Risk: The skill requires a CAMINO_API_KEY for repeated API access.

Mitigation: Use a least-privilege API key, store it only in the intended environment configuration, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/skills/location-context)
- [Camino API key activation](https://app.getcamino.ai/skills/activate)
- [Camino trial API key endpoint](https://api.getcamino.ai/trial/start)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON API responses with Markdown usage guidance and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CAMINO_API_KEY environment variable and sends requested location details to Camino AI.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
