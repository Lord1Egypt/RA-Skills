## Description: <br>
Migration guide for developers moving from Google Maps Platform to Mapbox GL JS, covering API equivalents, pattern translations, and key differences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute migrations from Google Maps Platform implementations to Mapbox GL JS, including API replacements, coordinate and event changes, markers, popups, clustering, geocoding, directions, styling, and performance patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser examples use Mapbox access tokens, and copied production code can accidentally expose secret tokens. <br>
Mitigation: Use scoped public Mapbox tokens in browser code and keep secret tokens server-side. <br>
Risk: Popup examples that render HTML can expose applications to unsafe content if populated with untrusted data. <br>
Mitigation: Sanitize untrusted popup content before using HTML rendering, or use text rendering when rich HTML is not required. <br>
Risk: Migration examples are reference guidance and may not cover every production behavior in an existing Google Maps implementation. <br>
Mitigation: Review adapted code, test feature parity, and scan the final application before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mapbox/mapbox-google-maps-migration) <br>
- [Mapbox publisher profile](https://clawhub.ai/user/mapbox) <br>
- [Mapbox GL JS Documentation](https://docs.mapbox.com/mapbox-gl-js/) <br>
- [Official Google Maps to Mapbox Migration Guide](https://docs.mapbox.com/help/tutorials/google-to-mapbox/) <br>
- [Mapbox GL JS Examples](https://docs.mapbox.com/mapbox-gl-js/examples/) <br>
- [Mapbox Style Specification](https://docs.mapbox.com/mapbox-gl-js/style-spec/) <br>
- [API Services, Pricing, Plugins, Framework Integration, and Testing](references/api-services.md) <br>
- [Clustering and Styling](references/clustering-styling.md) <br>
- [Data Updates, Performance, and Common Migration Patterns](references/data-performance.md) <br>
- [Directions, Routing, and Controls](references/directions-controls.md) <br>
- [Shapes, Custom Icons, and Geocoding](references/shapes-geocoding.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with JavaScript, HTML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only migration guidance; examples may require adaptation before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
