## Description:

Use when you need OpenStreetMap geocoding or annotated map generation for a set of places.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poxenstudio](https://clawhub.ai/user/poxenstudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up place coordinates and generate annotated OpenStreetMap-based map images from named or coordinate-based points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to OpenStreetMap, Nominatim, and tile endpoints.

Mitigation: Install and run it only where those network calls are approved, and keep request frequency under operator control.

Risk: Rendering can write requested PNG output paths and can emit large base64 image payloads.

Mitigation: Prefer reviewed output locations and normal PNG file delivery; use base64 output only when file delivery is unavailable.

Risk: Very large or untrusted point sets can increase network, rendering, and token costs.

Mitigation: Limit point-set size and keep width, height, and base64 options under operator control.

## Reference(s):

- [OpenStreetMap](https://openstreetmap.org)
- [Nominatim search endpoint](https://nominatim.openstreetmap.org/search)
- [OpenStreetMap tile endpoint](https://tile.openstreetmap.org/{z}/{x}/{y}.png)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with CLI examples; runtime output is JSON and optional PNG file or base64-encoded PNG.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default file output is recommended; base64 image output can be large and should be used only when file delivery is unavailable.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
