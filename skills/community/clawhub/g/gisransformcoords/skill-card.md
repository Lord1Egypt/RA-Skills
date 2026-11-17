## Description:

Converts GeoJSON point, line, and polygon coordinates between WGS84 (EPSG:4326) and Web Mercator (EPSG:3857) for WebGIS and GPS data workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pointgh](https://clawhub.ai/user/pointgh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and GIS practitioners use this skill to convert GeoJSON geometries and feature collections between geographic coordinates and Web Mercator for web maps, GPS processing, and vector-data preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The coordinate conversion script depends on pyproj, so an unreviewed or unpinned dependency version could change behavior or introduce supply-chain risk.

Mitigation: Install dependencies in a virtual environment and prefer a pinned, reviewed pyproj version.

Risk: Using the output-file option writes directly to the selected path and can overwrite existing data.

Mitigation: Choose a new output path or back up existing GeoJSON files before using -o or --output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pointgh/skills/gisransformcoords)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration guidance]

**Output Format:** [Markdown guidance with inline bash commands and GeoJSON JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write converted GeoJSON to stdout or to a user-specified output file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
