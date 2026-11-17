## Description:

High-performance Node.js implementation for monitoring Vietnamese Air Quality Indexes, with localized city mapping and multi-parameter environmental data retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guchigangz](https://clawhub.ai/user/guchigangz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query real-time air quality data for supported Vietnamese cities and return an interpreted AQI result for downstream user-facing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City queries are sent to the WAQI API.

Mitigation: Inform users that city lookups leave the local environment and require outbound access to https://api.waqi.info.

Risk: The bundled WAQI token is exposed in the source.

Mitigation: Prefer a release that uses a user-provided secret from the environment and rotates the exposed token before deployment.

Risk: Network calls do not document request timeouts or response-size limits.

Mitigation: Add operational controls for request timeout, response-size limits, and failure handling before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guchigangz/skills/js-hanoi-air)
- [Project homepage](https://github.com/picoclaw-skill/aqi-hanoi)
- [WAQI API](https://api.waqi.info)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns AQI, city, health level, selected weather fields, main pollutant, update timestamp, or an error message.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 3.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
