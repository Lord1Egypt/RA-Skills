## Description:

Control Hantek DSO2D15 / DSO2000-series oscilloscopes over USB SCPI, including connection checks, channel/generator setup, waveform capture, probe compensation guidance, and remote-control lock handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessehornbuckle](https://clawhub.ai/user/jessehornbuckle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and electronics technicians use this skill to connect to Hantek DSO2D15/DSO2000-series oscilloscopes, configure SCPI/VISA sessions, capture waveforms, and troubleshoot remote-control behavior during low-voltage bench diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python dependency installation may introduce unreviewed packages into the user's environment.

Mitigation: Use a dedicated virtual environment and prefer pinned, reviewed package versions.

Risk: SCPI commands may change oscilloscope settings on connected or powered equipment.

Mitigation: Review commands before sending them to the instrument and confirm read-only communication with an identity query first.

Risk: Oscilloscope ground connections can short circuits during live diagnostics.

Mitigation: Warn before safety-sensitive probing and use current-limited or fused power where practical.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline shell, Python, and SCPI command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include direct safety warnings before safety-sensitive probing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
