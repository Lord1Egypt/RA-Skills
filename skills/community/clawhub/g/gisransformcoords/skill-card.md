## Description: <br>
GIS 坐标转换工具，支持点、线、面 GeoJSON 数据在 WGS84（经纬度）和 Web Mercator（EPSG:3857）之间批量转换。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pointGH](https://clawhub.ai/user/pointGH) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and GIS practitioners use this skill to convert GeoJSON geometries between GPS-friendly WGS84 coordinates and Web Mercator coordinates used by common web mapping systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local GeoJSON input path supplied by the user. <br>
Mitigation: Run it only on intended local files and review the selected input path before execution. <br>
Risk: The skill can overwrite the output path supplied with the command. <br>
Mitigation: Choose output filenames deliberately, avoid existing important files, and validate converted GeoJSON before relying on it. <br>
Risk: The script depends on pyproj being installed in the execution environment. <br>
Mitigation: Install pyproj from a trusted package source, preferably inside a virtual environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pointGH/gisransformcoords) <br>
- [Publisher profile](https://clawhub.ai/user/pointGH) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and GeoJSON JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The conversion script can write a GeoJSON output file or print converted GeoJSON to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
