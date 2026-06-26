## Description: <br>
Guide for migrating from MapLibre GL JS to Mapbox GL JS, covering API compatibility, token setup, style configuration, and the benefits of Mapbox's official support and ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to migrate web maps from MapLibre GL JS to Mapbox GL JS, including package changes, imports, access token setup, style URLs, and plugin replacements. It helps teams understand which map APIs usually remain compatible and where Mapbox-specific configuration is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copying token examples into source control can expose Mapbox access tokens. <br>
Mitigation: Use environment variables, keep tokens out of git, restrict public tokens by domain, and rotate any token that may have been exposed. <br>
Risk: Using Mapbox geocoding, routing, search, or precise-location features may send user location data or addresses to Mapbox services. <br>
Mitigation: Review Mapbox privacy terms, add user notice or consent where needed, and avoid sending unnecessary sensitive location data. <br>
Risk: Migrating from MapLibre to Mapbox introduces Mapbox-specific licensing, pricing, token, and service-dependency considerations. <br>
Mitigation: Confirm that Mapbox commercial terms, pricing, billing alerts, and operational dependencies fit the application before applying the migration. <br>


## Reference(s): <br>
- [API Compatibility Matrix](references/api-compatibility.md) <br>
- [Mapbox-Exclusive Features](references/exclusive-features.md) <br>
- [Why Choose Mapbox](references/why-mapbox.md) <br>
- [Mapbox GL JS Documentation](https://docs.mapbox.com/mapbox-gl-js/) <br>
- [Mapbox GL JS API Reference](https://docs.mapbox.com/mapbox-gl-js/api/) <br>
- [Mapbox GL JS Examples](https://docs.mapbox.com/mapbox-gl-js/examples/) <br>
- [Mapbox Studio](https://studio.mapbox.com/) <br>
- [Mapbox GL JS GitHub Repository](https://github.com/mapbox/mapbox-gl-js) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with JavaScript, HTML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only migration guidance; no files are generated unless the agent applies suggested commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
