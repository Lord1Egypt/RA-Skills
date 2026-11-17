## Description:

LeafEngines provides a remote MCP/API integration for agricultural intelligence, including soil analysis, weather forecasts, crop recommendations, environmental scoring, farm planning, and TurboQuant capability checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwarranto](https://clawhub.ai/user/qwarranto)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and AI agents use this skill to connect Claude or OpenClaw to LeafEngines for agricultural planning, environmental analysis, and farm operations guidance. Typical tasks include soil analysis, weather-aware irrigation planning, crop recommendations, pest detection, yield prediction, market price lookup, sustainability scoring, and farm planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Farm coordinates, site details, photos, and operational data may be sent to a remote commercial API.

Mitigation: Submit only data intended to be shared with LeafEngines, and review the provider's privacy, retention, and pricing terms before use.

Risk: Agricultural, weather, pest, yield, and market outputs may be incomplete, stale, or unsuitable for a specific site.

Mitigation: Treat outputs as decision support and validate important operational decisions against local expertise, field measurements, and current market or weather sources.

Risk: API keys are required for authenticated use and may be exposed if placed in shared configuration files or logs.

Mitigation: Store API keys in private local configuration or a secret manager, rotate compromised keys, and avoid committing credentials.

## Reference(s):

- [LeafEngines API Reference](references/API_REFERENCE.md)
- [LeafEngines ClawHub Skill Page](https://clawhub.ai/qwarranto/skills/leafengines-clawhub-skill)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, YAML configuration snippets, shell commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an x-api-key for authenticated LeafEngines API use; access and rate limits depend on the user's subscription tier.]

## Skill Version(s):

1.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
