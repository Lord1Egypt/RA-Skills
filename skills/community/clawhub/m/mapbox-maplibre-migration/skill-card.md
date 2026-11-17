## Description:

Guide for migrating from MapLibre GL JS to Mapbox GL JS, covering API compatibility, token setup, style configuration, and the benefits of Mapbox's official support and ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate web mapping applications from MapLibre GL JS to Mapbox GL JS, including package changes, token setup, style updates, plugin swaps, and compatibility checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mapbox access tokens can be exposed, committed, or scoped too broadly in client applications.

Mitigation: Use public client tokens for browser code, store tokens in environment variables, add URL restrictions, avoid committing .env files, and rotate tokens if compromised.

Risk: Migrating to Mapbox services can send map, geocoding, or related API traffic to Mapbox and may affect usage or billing.

Mitigation: Review Mapbox service fit and pricing before deployment, monitor usage, and set billing alerts for production applications.

Risk: Incorrect package, plugin, token, or style changes can break maps after migration.

Mitigation: Test map initialization, tile loading, custom sources and layers, events, popups, and Mapbox plugin equivalents before release.

## Reference(s):

- [API Compatibility Matrix](references/api-compatibility.md)
- [Mapbox-Exclusive Features](references/exclusive-features.md)
- [Why Choose Mapbox](references/why-mapbox.md)
- [Mapbox GL JS Documentation](https://docs.mapbox.com/mapbox-gl-js/)
- [Mapbox GL JS Examples](https://docs.mapbox.com/mapbox-gl-js/examples/)
- [Mapbox GL JS API Reference](https://docs.mapbox.com/mapbox-gl-js/api/)
- [Mapbox Studio](https://studio.mapbox.com/)
- [Mapbox GL JS GitHub Repository](https://github.com/mapbox/mapbox-gl-js)
- [Mapbox Pricing](https://www.mapbox.com/pricing/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, HTML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; may recommend package installs, token configuration, Mapbox API/CDN calls, and review of pricing or billing impacts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
