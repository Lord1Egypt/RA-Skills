## Description: <br>
Network health monitoring for Pilot Protocol agents with latency, reachability, routing, throughput, daemon, connection, and peer checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose Pilot Protocol connectivity issues, monitor network health, and inspect daemon, peer, and active connection status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Peer, connection, traceroute, and recent-contact checks may reveal internal network topology or operational metadata. <br>
Mitigation: Run checks only on Pilot Protocol networks and agents you are authorized to inspect, and avoid sharing raw output that exposes internal topology. <br>
Risk: Health results depend on pilotctl, the Pilot Protocol core skill, a running daemon, and reachable target agents. <br>
Mitigation: Confirm pilotctl is available, the daemon is running, and targets are authorized and reachable before relying on the results. <br>


## Reference(s): <br>
- [Pilot Protocol Homepage](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-health) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses pilotctl JSON command output for network health interpretation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; SKILL.md frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
