## Description: <br>
Controls Netatmo thermostat settings and reads weather station data including temperature, CO2, humidity, noise, pressure, and history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[florianbeer](https://clawhub.ai/user/florianbeer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and smart-home operators use this skill to check Netatmo sensor readings and manage thermostat temperature or modes through the local netatmo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a separate local netatmo CLI and token files in ~/.config/netatmo/. <br>
Mitigation: Install only trusted CLI builds and protect credential and token files with appropriate local filesystem permissions. <br>
Risk: Thermostat commands can change heating temperature or mode. <br>
Mitigation: Require explicit confirmation before temperature or mode changes when accidental heating changes would matter. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON output from the netatmo CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensor readings, thermostat mode or temperature actions, and history summaries with ASCII sparklines.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
