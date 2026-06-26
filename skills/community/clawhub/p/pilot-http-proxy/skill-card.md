## Description: <br>
Routes HTTP requests through Pilot Protocol tunnels using the gateway subsystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route HTTP traffic through Pilot Protocol tunnels when accessing services behind NATs or firewalls, or when exposing local HTTP servers to remote agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mapping sensitive or unauthenticated internal HTTP services through the gateway can expose them beyond the intended network boundary. <br>
Mitigation: Map only intended services, prefer authenticated TLS endpoints, verify who can reach each mapped service, and unmap or stop the gateway when finished. <br>
Risk: Forwarding common HTTP ports may require elevated privileges on Linux for ports below 1024. <br>
Mitigation: Use the least privilege needed, avoid privileged ports when possible, and review gateway commands before execution. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilotctl binary, the pilot-protocol skill, and a running Pilot daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
