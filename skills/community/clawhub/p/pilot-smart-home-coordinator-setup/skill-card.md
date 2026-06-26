## Description: <br>
Deploy a four-agent Pilot Protocol smart home coordinator that connects sensor, brain, actuator, and dashboard roles for home automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home operators use this skill to set up coordinated Pilot Protocol agents that collect sensor readings, resolve home-control goals, execute device commands, and report status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Smart-home reporting can expose sensitive occupancy, lock-state, room-activity, or device-status data through Slack, email, or webhook destinations. <br>
Mitigation: Review downstream bridge skills before enabling external reporting, trust the destination, and configure redaction or aggregation before sending home data outside the local network. <br>
Risk: Device-command workflows can affect physical home systems such as HVAC, lighting, locks, and shutters. <br>
Mitigation: Confirm handshakes and role manifests before use, and review actuator commands and audit logs before relying on automated device actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-smart-home-coordinator-setup) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON manifest examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, clawhub, and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
