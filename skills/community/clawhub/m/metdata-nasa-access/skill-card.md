## Description: <br>
Fetch NASA POWER meteorological data for wind and solar energy, output Excel files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuepeng1985-web](https://clawhub.ai/user/yuepeng1985-web) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and renewable-energy analysts use this skill to resolve a place name or coordinates, fetch NASA POWER wind and solar meteorological data, and produce structured Excel workbooks for PV or wind assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Entered place names or coordinates are sent to OpenStreetMap Nominatim and NASA POWER. <br>
Mitigation: Use approximate coordinates or a less precise area for sensitive home, workplace, or customer locations. <br>
Risk: Generated Excel files remain on disk at the selected output path. <br>
Mitigation: Choose the output path deliberately and handle generated files according to the sensitivity of the location and weather data. <br>


## Reference(s): <br>
- [NASA POWER](https://power.larc.nasa.gov) <br>
- [OpenStreetMap Nominatim Search](https://nominatim.openstreetmap.org/search) <br>
- [ClawHub skill listing](https://clawhub.ai/yuepeng1985-web/metdata-nasa-access) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, files] <br>
**Output Format:** [Markdown guidance with bash commands and generated Excel workbook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Excel output contains monthly, daily, and climatological sheets when all granularities are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
