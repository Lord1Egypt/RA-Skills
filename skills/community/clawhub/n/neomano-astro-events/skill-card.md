## Description: <br>
Astronomy visibility helper for a given location (lat/lon). Lists what you can see tonight and in the next days: Moon phase and rise/set, planet visibility windows, and optional ISS passes. Use when the user asks for astronomical events visible from their coordinates/city. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elandivar](https://clawhub.ai/user/elandivar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to compute local sky visibility for a specified latitude, longitude, timezone, and date range, including moon information, planet viewing windows, twilight transitions, and ISS passes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script creates a local Python virtual environment and installs unpinned Python dependencies. <br>
Mitigation: Review the dependency installation step before use and run it in a controlled local environment. <br>
Risk: The skill downloads public astronomy datasets during normal operation, including Skyfield ephemeris data and ISS TLE data from Celestrak. <br>
Mitigation: Allow only the disclosed outbound dataset downloads needed for astronomy calculations. <br>


## Reference(s): <br>
- [Celestrak Stations TLE Data](https://celestrak.org/NORAD/elements/stations.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text reports with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports twilight transitions, moon phase, planet viewing windows, and ISS pass times; requires local Python setup and public astronomy data downloads.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
