## Description: <br>
Simple smoke/fire detector for living room. Queries Dirigera air sensor every 5 minutes, detects dangerous PM2.5 over 250 or CO2 over 2000 levels, and broadcasts emergency alert on Mac speaker continuously until air quality normalizes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-2](https://clawhub.ai/user/maverick-2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Home automation users and maintainers use this skill to monitor a living-room Dirigera air sensor and trigger a local Mac audio alert when PM2.5 or CO2 readings exceed configured danger thresholds. It is a backup alarm workflow, not a certified smoke detector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a local Dirigera hub bearer token for sensor access. <br>
Mitigation: Install only on a trusted machine and network, protect the token file, and rotate the token if it may have been exposed. <br>
Risk: The sensor request disables TLS certificate and hostname verification. <br>
Mitigation: Verify the hub IP before use and prefer a version that validates or pins the hub certificate before relying on it. <br>
Risk: The alert workflow is safety-related but is not a certified smoke detector. <br>
Mitigation: Use it only as a local backup alarm alongside certified smoke detectors and established emergency procedures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-2/living-room-smoke-detector) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local JSON state output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs against a local Dirigera hub and writes detector state to data/detector_state.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
