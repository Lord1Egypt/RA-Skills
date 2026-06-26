## Description: <br>
Build, debug, and integrate Leaflet web maps across vanilla HTML, Vite, React, and other frontend apps, including setup, tile layers, markers, popups, GeoJSON overlays, bounds fitting, event handling, and plugin-safe patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, debug, and integrate practical 2D Leaflet maps with tile layers, markers, popups, GeoJSON overlays, framework lifecycle handling, and plugin-aware implementation patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated map code may omit required tile-provider attribution or use a provider outside its terms. <br>
Mitigation: Review the selected tile provider's attribution and usage terms, then keep the tile URL and attribution configurable. <br>
Risk: Popup content or GeoJSON feature properties from untrusted data may introduce unsafe HTML into a map. <br>
Mitigation: Escape or sanitize untrusted popup and property content before rendering it in Leaflet. <br>
Risk: Examples adapted for production could accidentally hardcode private tokens, private tile servers, or machine-specific paths. <br>
Mitigation: Move secrets and environment-specific values into configuration and review generated code before deployment. <br>


## Reference(s): <br>
- [Leaflet Documentation](https://leafletjs.com/) <br>
- [Leaflet Patterns](references/patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jvy/leaflet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include targeted debugging analysis, minimal reproducible Leaflet examples, framework lifecycle notes, and tile-provider or CRS assumptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
