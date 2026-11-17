## Description:

Helps agents build, debug, and integrate Mapbox apps and APIs, including GL JS map setup, styles, sources and layers, markers and popups, geocoding, directions, static images, and token-safe frontend patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement, debug, and explain Mapbox web maps and API integrations while keeping access tokens configurable and scoped.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Mapbox examples may expose or hardcode access tokens if users paste real credentials or request local-only demos.

Mitigation: Keep tokens in environment or runtime configuration, restrict public tokens by allowed URLs where possible, and avoid reprinting secret tokens.

Risk: Incorrect Mapbox setup guidance can lead to blank maps, invisible layers, wrong locations, or unnecessary API calls.

Mitigation: Start with a minimal working map, confirm container sizing, token scopes, style and source IDs, coordinate order, layer order, rate limits, and request parameters.

## Reference(s):

- [Mapbox Patterns](references/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/jvy/skills/mapbox)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Mapbox GL JS snippets, API integration guidance, troubleshooting checks, and token-handling recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
