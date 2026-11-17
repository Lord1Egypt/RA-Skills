## Description:

Builds Aloudata CAN semantic-layer metric query requests by first retrieving metric and dimension metadata from the Aloudata Gateway, then producing query bodies for metric data analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackyujun](https://clawhub.ai/user/jackyujun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to translate natural-language metric questions into Aloudata CAN Gateway searches and metric query JSON. It is intended for workflows that need metric selection, compatible dimensions, filters, time constraints, comparisons, proportions, rankings, or temporary metric definitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Metric names, dimension values, filters, and query bodies are sent to the Aloudata Gateway.

Mitigation: Use the skill only with data intended for that gateway and avoid prompts containing unrelated secrets or highly sensitive business identifiers.

Risk: The skill requires a user-provided CAN_API_KEY for Gateway access.

Mitigation: Configure CAN_API_KEY as a dedicated, least-privilege credential and prefer the X-API-Key request header.

Risk: Incorrect metric or dimension selection can produce misleading analytics results.

Mitigation: Follow the skill's requirement to retrieve metric and dimension metadata before constructing queries and return an empty JSON object when required context is missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackyujun/skills/metric-query)
- [Aloudata homepage](https://aloudata.com/)
- [Aloudata Gateway metrics query API](https://gateway.can.aloudata.com/api/metrics/query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON request bodies and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return an empty JSON object when metric or dimension evidence is insufficient for a valid query.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
