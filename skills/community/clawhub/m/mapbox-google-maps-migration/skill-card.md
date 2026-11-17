## Description:

Migration guide for developers moving from Google Maps Platform to Mapbox GL JS, covering API equivalents, pattern translations, and key differences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute migrations from Google Maps Platform to Mapbox GL JS. It helps translate initialization, markers, popups, events, shapes, geocoding, directions, clustering, styling, and performance patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied examples may expose or mishandle Mapbox access tokens in real applications.

Mitigation: Review token handling before deployment, use appropriate public tokens for client-side code, and apply project-specific token restrictions.

Risk: Geocoding and directions examples may send location data to Mapbox services.

Mitigation: Disclose Mapbox data sharing where required and avoid sending sensitive location data unless it is necessary for the application.

Risk: Popup examples that render HTML can introduce unsafe content handling if populated with untrusted data.

Mitigation: Sanitize popup content or use text-only rendering for untrusted values.

## Reference(s):

- [Mapbox Google Maps Migration Skill](https://clawhub.ai/mapbox/skills/mapbox-google-maps-migration)
- [Mapbox Publisher Profile](https://clawhub.ai/user/mapbox)
- [Mapbox GL JS Documentation](https://docs.mapbox.com/mapbox-gl-js/)
- [Official Google Maps to Mapbox Migration Guide](https://docs.mapbox.com/help/tutorials/google-to-mapbox/)
- [Mapbox GL JS Examples](https://docs.mapbox.com/mapbox-gl-js/examples/)
- [Mapbox Style Specification](https://docs.mapbox.com/mapbox-gl-js/style-spec/)
- [API Services, Pricing, Plugins, Framework Integration, and Testing](references/api-services.md)
- [Clustering and Styling](references/clustering-styling.md)
- [Data Updates, Performance, and Common Migration Patterns](references/data-performance.md)
- [Directions, Routing, and Controls](references/directions-controls.md)
- [Shapes, Custom Icons, and Geocoding](references/shapes-geocoding.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JavaScript, HTML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include migration checklists, API-equivalence tables, and Mapbox GL JS implementation snippets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
