## Description: <br>
Assign and manage hierarchical roles within a swarm for coordinated task distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing Pilot Protocol swarms use this skill to advertise agent capabilities, assign leader, worker, or coordinator roles, and inspect current role distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing capabilities and role assignments can expose operational metadata or affect role coordination if sent through untrusted registries or peers. <br>
Mitigation: Use the skill only in trusted Pilot Protocol swarms, minimize published agent metadata, and prefer authenticated, encrypted, access-controlled channels. <br>
Risk: The guidance includes network messaging commands that can change agent roles when executed. <br>
Mitigation: Review command targets, swarm names, agent addresses, and JSON payloads before execution. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon, jq, base64, and trusted swarm or registry endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
