## Description:

Unified information services hub combining location, weather, and time capabilities with multi-source geolocation, fixed-point weather forecasts, and multi-source time reporting with confidence scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route location, weather, and time requests through one interface and receive structured results with confidence scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect precise location data and send location or time queries to external providers.

Mitigation: Ask for user consent before using current-location sources, prefer manual city or coarse location when sufficient, and disclose which provider receives each query.

Risk: Broad requests can trigger multiple services and disclose more context than the user intended.

Mitigation: Route to the narrowest matching service by default and run all services only when the user explicitly requests combined location, weather, and time output.

Risk: Optional geolocation provider credentials may be required for enhanced accuracy.

Mitigation: Store credentials only in environment variables and avoid echoing, logging, or including API keys in outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnsmithfan/skills/information-services)
- [Location Service specifications](artifact/references/location.md)
- [Weather Service specifications](artifact/references/weather.md)
- [Time Service specifications](artifact/references/time.md)
- [Method Patterns and Coordination](artifact/references/method-patterns.md)

## Skill Output:

**Output Type(s):** [text, guidance, configuration, shell commands]

**Output Format:** [JSON service results and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured service results include service_type, data, confidence, and timestamps when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
