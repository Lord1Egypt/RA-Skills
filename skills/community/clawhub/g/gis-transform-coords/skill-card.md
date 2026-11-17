## Description:

Converts GeoJSON point, line, and polygon data between WGS84 (EPSG:4326) and Web Mercator (EPSG:3857) for batch GIS workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pointgh](https://clawhub.ai/user/pointgh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and GIS practitioners use this skill to convert GeoJSON geometries for WebGIS maps, GPS data display, and batch vector-data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency or environment drift can affect coordinate conversion behavior.

Mitigation: Install pyproj in a dedicated virtual environment and pin a reviewed version before use.

Risk: Running the converter on unintended paths can read or overwrite local GeoJSON files.

Mitigation: Run it only against intended GeoJSON inputs and explicitly chosen output paths.

Risk: The usage documentation is primarily Chinese, which may cause setup or operation errors for non-Chinese readers.

Mitigation: Translate and review command usage before relying on the skill in multilingual teams.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pointgh/skills/gis-transform-coords)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands and GeoJSON/JSON file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces converted GeoJSON to stdout or an output file; supports pretty-printed JSON.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
