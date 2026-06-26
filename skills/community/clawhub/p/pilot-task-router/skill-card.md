## Description: <br>
Route tasks to the best agent by capability and reputation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to discover qualified Pilot Protocol peers, rank them by capability and reputation, and submit tasks to a selected agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routed task descriptions may be sent to selected Pilot Protocol peers. <br>
Mitigation: Avoid including secrets, private data, credentials, or irreversible instructions in routed tasks. <br>
Risk: Routing depends on discoverable peers and local pilotctl output, so an unsuitable or unavailable peer may be selected. <br>
Mitigation: Review the selected peer before submitting sensitive work and keep fallback routing scoped to trusted peers. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-task-router) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses pilotctl and jq; routed task content may be sent to selected peers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
