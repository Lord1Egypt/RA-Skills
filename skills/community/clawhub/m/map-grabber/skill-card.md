## Description: <br>
Fetch OpenStreetMap vector data for an address or place name and export street networks, optional building footprints, and preview maps as PNG, SVG, GeoPackage, or DXF files for CAD and Rhino workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QROST](https://clawhub.ai/user/QROST) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, designers, and architecture/CAD users use this skill to fetch site base maps around an address or place name, including street networks and optional building footprints. Agents can generate preview images for chat and vector files for downstream CAD or Rhino workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Address or place-name inputs may be sent to external OpenStreetMap-related services during geocoding and map retrieval. <br>
Mitigation: Use the skill only when sharing the requested location with those services is acceptable. <br>
Risk: Generated CAD and map files may contain incomplete, stale, or imprecise OpenStreetMap-derived data. <br>
Mitigation: Review generated PNG, SVG, GeoPackage, or DXF outputs before relying on them in CAD or Rhino workflows. <br>
Risk: Runtime behavior depends on local Python packages such as osmnx and ezdxf. <br>
Mitigation: Install dependencies in a controlled environment and pin versions when reproducible outputs are required. <br>


## Reference(s): <br>
- [Map Grabber on ClawHub](https://clawhub.ai/QROST/map-grabber) <br>
- [QROST publisher profile](https://clawhub.ai/user/QROST) <br>
- [QROST GitHub profile](https://github.com/QROST) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG, SVG, GeoPackage, or DXF files with concise text confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an address or place name and at least one requested output path; optional radius and building-footprint settings control map scope.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
