## Description: <br>
Monitors live status of a Pod Point charger's connectors A and B, reporting current availability and changes without requiring authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoranjurcevic](https://clawhub.ai/user/zoranjurcevic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Drivers and agents use this skill to check whether a specific Pod Point charging pod is available. It can return the current connector A/B status or watch for availability changes using a provided pod ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watch mode repeatedly contacts Pod Point until the timeout expires. <br>
Mitigation: Use reasonable intervalSeconds and timeoutSeconds values. <br>
Risk: The provided pod ID is sent to Pod Point's public status endpoint. <br>
Mitigation: Only provide pod IDs you are comfortable sending to Pod Point. <br>


## Reference(s): <br>
- [Podpoint on ClawHub](https://clawhub.ai/zoranjurcevic/podpoint) <br>
- [Publisher profile](https://clawhub.ai/user/zoranjurcevic) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, status information, notifications] <br>
**Output Format:** [JSON object with connector status, availability flags, and optional event details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a podId. Watch mode polls Pod Point until the configured timeout expires.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
