## Description:

Visualizes GPS track routes from KML or GPX files by parsing route points, computing route statistics, and generating static JPG maps or interactive HTML maps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziemen](https://clawhub.ai/user/ziemen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn GPX or KML route data into route maps, elevation profiles, and summary statistics for hiking, running, cycling, and other GPS track workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GPX, KML, and generated track JSON can expose precise locations, route habits, and local file path metadata.

Mitigation: Treat route inputs and generated outputs as sensitive, remove or replace real sample route data before broad distribution, and avoid sharing generated files unless location data has been reviewed.

Risk: Interactive HTML maps may contact external map tile services when opened.

Mitigation: Use the interactive HTML output only when external tile requests are acceptable, or prefer static JPG output for offline review.

Risk: Generated HTML from untrusted track JSON may carry content into a browser context.

Mitigation: Avoid opening generated HTML from untrusted inputs and run the workflow in an isolated Python environment with pinned dependencies.

## Reference(s):

- [KML / GPX File Format Reference](references/formats.md)
- [ClawHub skill page](https://clawhub.ai/ziemen/skills/gpx-kml-visualizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file output guidance for JSON, JPG, and HTML artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated interactive maps may request external map tiles, and generated route files can contain precise GPS data.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
