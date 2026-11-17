## Description:

Control Netatmo thermostat and read weather station data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[florianbeer](https://clawhub.ai/user/florianbeer)

### License/Terms of Use:


## Use Case:

External users use this skill to inspect Netatmo thermostat and weather station readings, including temperature, humidity, CO2, noise, pressure, and battery data. It can also guide thermostat actions such as changing target temperature or mode through the local netatmo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Thermostat set and mode commands can immediately change heating behavior.

Mitigation: Confirm the intended temperature or mode before running set or mode commands.

Risk: The local Netatmo configuration stores account credentials and OAuth tokens.

Mitigation: Keep ~/.config/netatmo protected and limit access to users who should control the Netatmo account and thermostat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/florianbeer/skills/netatmo)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown, JSON]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or recommend commands that read Netatmo device state or change thermostat settings through the local netatmo CLI.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
