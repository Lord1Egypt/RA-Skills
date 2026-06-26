## Description: <br>
Full IPFS node operations -- install, configure, pin content, publish IPNS, manage peers, and run gateway services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apexfork](https://clawhub.ai/user/apexfork) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, server administrators, and infrastructure operators use this skill to run and maintain IPFS nodes, publish and pin content, configure gateways, manage peers, and troubleshoot node health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation and daemon-management commands can change the local system or start long-running network services. <br>
Mitigation: Review each command before execution, confirm the Kubo download source, and run the skill only when operating an IPFS node is intended. <br>
Risk: Gateway, API, and swarm configuration can expose services to local networks or the public internet. <br>
Mitigation: Bind API and gateway endpoints to localhost unless public access is intentional, restrict exposed ports with firewall rules, and monitor bandwidth and storage usage. <br>
Risk: Remote pinning examples involve service tokens or JWTs. <br>
Mitigation: Pass real pinning credentials through environment variables or a secret manager instead of typing secrets directly into commands. <br>


## Reference(s): <br>
- [IPFS Server on ClawHub](https://clawhub.ai/apexfork/ipfs-server) <br>
- [apexfork Publisher Profile](https://clawhub.ai/user/apexfork) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational cautions for network exposure, storage, bandwidth, and secret handling.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
