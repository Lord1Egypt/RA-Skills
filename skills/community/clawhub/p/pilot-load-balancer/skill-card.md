## Description: <br>
Distribute tasks across worker pools with health-aware load balancing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and engineers use this skill to distribute tasks across worker agents, choose round-robin or least-connections routing, and avoid overloading worker pools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task assignments are sent to discovered worker addresses, so stale status data or broad search filters can route work to unintended or overloaded workers. <br>
Mitigation: Review worker filters and status inputs before use, verify the target pool, and start with a small batch before scaling assignment volume. <br>
Risk: The workflow depends on local command-line tools and a running daemon; missing prerequisites can cause failed or inconsistent load balancing. <br>
Mitigation: Confirm pilotctl, jq, uuidgen, the pilot-protocol skill, and daemon health before running the command sequence. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilot-protocol skill, pilotctl, jq, uuidgen, and a running pilotctl daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
