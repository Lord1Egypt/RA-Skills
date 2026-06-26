## Description: <br>
Join or create agent swarms with auto-discovery and peer mesh formation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and engineers use this skill to join or create named Pilot Protocol swarms, discover peers, and establish mesh trust among intended swarm members. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The approve-all peer trust command can approve unintended pending nodes. <br>
Mitigation: Inspect pending requests, verify swarm membership and node identity, and approve only specific trusted peers. <br>
Risk: Swarm join commands can expose the agent to peers through the configured registry and daemon. <br>
Mitigation: Use the skill only with a controlled pilotctl daemon, intended registry, and understood peer trust model. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-swarm-join) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, jq, a running Pilot daemon, and access to the intended registry.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
