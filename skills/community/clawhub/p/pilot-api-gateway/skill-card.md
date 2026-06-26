## Description: <br>
Expose local APIs to the Pilot Protocol network through gateway mode or custom messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and engineers use this skill to make local API services reachable by remote Pilot agents without exposing the services directly on the public internet. It provides gateway startup, remote host mapping, and custom request/response handling commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make a local service reachable through a remote-access workflow. <br>
Mitigation: Confirm the exact local app, host, and port before exposing it; avoid admin, debug, or sensitive internal services. <br>
Risk: An exposed route may remain available after it is no longer needed. <br>
Mitigation: Stop the gateway or remove the route when sharing is finished, and keep the pilotctl daemon limited to intended use. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilot-protocol skill, pilotctl on PATH, a running pilotctl daemon, and a local API server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
