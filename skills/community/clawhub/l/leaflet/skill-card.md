## Description:

Build, debug, and integrate Leaflet web maps for map setup, tile layers, markers, popups, GeoJSON overlays, bounds fitting, event handling, and frontend framework integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or troubleshoot practical 2D Leaflet maps in frontend apps, including tiles, markers, popups, GeoJSON overlays, sizing issues, and SPA lifecycle handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated map examples can omit or misuse tile-provider terms, attribution, rate limits, or private service tokens.

Mitigation: Review provider terms, include required attribution, and keep tile URLs and tokens configurable before production use.

Risk: Popup or feature-property examples can expose raw untrusted HTML.

Mitigation: Escape or sanitize user-provided feature properties before binding popup content.

Risk: Incorrect CRS or coordinate-order assumptions can place features in the wrong location.

Mitigation: Confirm WGS84 and GeoJSON coordinate order before rendering, and use a reprojection workflow when the source data uses another CRS.

## Reference(s):

- [Leaflet Homepage](https://leafletjs.com/)
- [Leaflet Patterns](references/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/jvy/skills/leaflet)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tile attribution, CRS assumptions, lifecycle cleanup notes, and security notes for token or tile-provider handling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
