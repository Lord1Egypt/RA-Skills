## Description: <br>
Detect agent failures and trigger automatic task redistribution or re-election. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to monitor swarm members with heartbeat messages, detect unreachable agents, verify failures, and support failover, load balancing, or leader election workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heartbeat publishing and failover checks can affect live task redistribution or leader election if run with the wrong swarm, registry, or agent identifiers. <br>
Mitigation: Review commands and environment variables before execution, and test heartbeat timeouts and failover behavior in a controlled swarm before production use. <br>
Risk: Failure detection depends on timeout settings and network conditions, which can produce false failure signals during delays or partitions. <br>
Mitigation: Tune heartbeat intervals and timeouts for the deployment, and verify suspected failures with direct ping checks before triggering recovery actions. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, jq, bc, and a running pilot-protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
