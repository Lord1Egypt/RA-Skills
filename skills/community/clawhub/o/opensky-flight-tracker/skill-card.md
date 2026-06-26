## Description: <br>
CLI skill for real-time flight tracking using the OpenSky Network API with no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javi23ruiz](https://clawhub.ai/user/javi23ruiz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to track live aircraft by radio callsign or flight number and to list airborne aircraft near supplied coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the required third-party PyPI package may introduce dependency supply-chain risk. <br>
Mitigation: Install in a managed or isolated environment and review the package source, version, and lockfile policy before deployment. <br>
Risk: Flight numbers, callsigns, or coordinates sent to the data source may reveal location-related interests. <br>
Mitigation: Avoid sensitive queries and confirm that external flight-tracking requests are acceptable for the intended environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/javi23ruiz/opensky-flight-tracker) <br>
- [Support issues](https://github.com/javi23ruiz/flight-tracker-cli/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; CLI output is human-readable summary text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the flight-tracker CLI. Queries may send callsigns, flight numbers, or coordinates to the flight-tracking data source.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
