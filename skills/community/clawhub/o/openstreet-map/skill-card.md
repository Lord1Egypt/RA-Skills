## Description: <br>
Provides OpenStreetMap geocoding and annotated map generation for a set of places. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poxenstudio](https://clawhub.ai/user/poxenstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to geocode place names with OpenStreetMap data and generate annotated map images from one or more places. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location queries and coordinates are sent to external map services during normal use. <br>
Mitigation: Use the skill only with location data appropriate to share with those services, and review privacy or compliance requirements before sending sensitive places. <br>
Risk: Rendered PNG files are written to a caller-provided output path. <br>
Mitigation: Run the skill in a controlled Python environment and use a dedicated output directory so generated files do not overwrite important files. <br>
Risk: Python dependencies may resolve differently over time. <br>
Mitigation: Pin dependency versions when reproducible installs are required. <br>


## Reference(s): <br>
- [Openstreet Map on ClawHub](https://clawhub.ai/poxenstudio/openstreet-map) <br>
- [OpenStreetMap](https://openstreetmap.org) <br>
- [Nominatim search endpoint](https://nominatim.openstreetmap.org/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands] <br>
**Output Format:** [JSON stdout with optional PNG file output or base64-encoded PNG in JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default to PNG file output; use base64 image output only when file delivery is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
