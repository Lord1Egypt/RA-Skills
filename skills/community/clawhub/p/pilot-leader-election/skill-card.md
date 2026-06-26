## Description: <br>
Elect a coordinator with automatic failover using heartbeat-based leader election. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to coordinate a swarm around a single leader, publish candidacy and heartbeat messages with pilotctl, and trigger failover when the current leader stops sending heartbeats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing election or heartbeat messages to a production registry host or shared ELECTION_GROUP can change the observed leader state for an active swarm. <br>
Mitigation: Test with a non-production registry host and an isolated ELECTION_GROUP before using the commands with production coordination topics. <br>
Risk: Incorrect timeout, term, priority, or tie-breaking values can cause premature failover or competing leadership announcements. <br>
Mitigation: Review election parameters, heartbeat intervals, and term handling before execution, and monitor inbox messages during rollout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-leader-election) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilotctl binary, the pilot-protocol skill, jq, cksum, and a running Pilot daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
