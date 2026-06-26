## Description: <br>
Converts GeoJSON point, line, and polygon data between WGS84 (EPSG:4326) and Web Mercator (EPSG:3857), including batch workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pointGH](https://clawhub.ai/user/pointGH) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and GIS practitioners use this skill to convert GeoJSON geometry and feature collections between GPS-friendly WGS84 coordinates and Web Mercator coordinates used by web mapping projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The command reads and writes local GeoJSON files, so an incorrect path can overwrite or expose unintended local data. <br>
Mitigation: Review input and output paths before running conversions, and write to a new output file when preserving the source matters. <br>
Risk: The script depends on pyproj, which must be installed separately. <br>
Mitigation: Install pyproj from a trusted package index and pin the dependency when reproducible environments are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pointGH/gis-transform-coords) <br>
- [Publisher profile](https://clawhub.ai/user/pointGH) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and GeoJSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces converted GeoJSON to stdout or an output file; supports pretty-printed JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
