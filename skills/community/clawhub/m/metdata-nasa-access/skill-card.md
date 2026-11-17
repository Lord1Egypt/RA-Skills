## Description:

Fetch NASA POWER meteorological data for wind and solar energy, output Excel files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuepeng1985-web](https://clawhub.ai/user/yuepeng1985-web)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and energy analysts use this skill to retrieve NASA POWER meteorological data for photovoltaic, wind, and weather assessment at a specified location. It resolves location names or coordinates, runs the bundled fetch script, and summarizes the generated Excel workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location names, precise addresses, or coordinates may be sent to external geocoding and meteorological data services.

Mitigation: Use direct coordinates when avoiding address disclosure is important, and inform users that coordinates are sent to NASA POWER for data retrieval.

Risk: The script writes an Excel workbook to the selected output path.

Mitigation: Choose an output path intentionally and review generated files before sharing them.

Risk: Generated workbook sheets use Chinese labels.

Mitigation: Confirm worksheet labels are appropriate for downstream users or rename sheets after generation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuepeng1985-web/skills/metdata-nasa-access)
- [NASA POWER](https://power.larc.nasa.gov)
- [OpenStreetMap Nominatim Search](https://nominatim.openstreetmap.org/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and generated Excel workbooks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Excel output may include monthly, daily, and climatological sheets with Chinese worksheet labels.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
