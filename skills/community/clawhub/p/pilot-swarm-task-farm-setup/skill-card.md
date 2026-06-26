## Description: <br>
Deploy a self-organizing Pilot Protocol compute swarm with five agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a five-agent Pilot Protocol task farm with one leader, three workers, and one monitor, including required skills, hostnames, manifests, trust handshakes, and example message flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Peer trust handshakes can authorize the wrong host if identities are not checked before setup. <br>
Mitigation: Verify each leader, worker, and monitor peer before running handshake commands. <br>
Risk: Port 1002 carries task assignments, results, and worker metrics between swarm nodes. <br>
Mitigation: Restrict port 1002 to trusted networks and hosts you control. <br>
Risk: Slack alerts can expose operational details if the bridge is misconfigured. <br>
Mitigation: Review the installed pilot-slack-bridge settings before sending alerts to Slack. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-swarm-task-farm-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON manifest templates and bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Assumes pilotctl, clawhub, the pilot-protocol skill, and a running daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
