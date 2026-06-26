## Description: <br>
Gossip protocol for eventually-consistent shared state propagation across swarms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and operators use this skill to propagate eventually consistent shared state across Pilot swarms by sending updates to random peer subsets and merging received state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gossiped agent state can spread to peers and peer state can be accepted without clear trust or validation safeguards. <br>
Mitigation: Use only with trusted Pilot swarms, add peer authentication and payload validation, and never include secrets or private operational data in shared state. <br>
Risk: Unbounded gossip fanout, rounds, or payload sizes can amplify incorrect state or overload participants. <br>
Mitigation: Keep fanout and rounds bounded, enforce payload size limits, and define conflict or rollback rules before relying on the state for important workflows. <br>


## Reference(s): <br>
- [Pilot Protocol Homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, jq, shuf, base64, and a running Pilot daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
