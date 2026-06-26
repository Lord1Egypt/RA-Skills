## Description: <br>
Comprehensive management for Portainer CE environments and stacks. Supports listing environments, managing Docker Compose/Swarm stacks, and executing raw Docker commands via proxy. Use when the user needs to deploy apps, check container status, or manage networks within Portainer. Requires a Portainer API Key configured in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leventsoft](https://clawhub.ai/user/Leventsoft) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to manage Portainer CE environments, inspect stacks, deploy Docker Compose content, remove stacks, and proxy selected Docker API requests through Portainer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Portainer and Docker administration can interrupt services or delete resources. <br>
Mitigation: Use a least-privilege Portainer token, restrict target environments, and require explicit confirmation before deploy, update, prune, remove, or raw Docker API operations. <br>
Risk: Weak transport security can expose sensitive API traffic. <br>
Mitigation: Enable real TLS certificate verification and avoid connecting to Portainer endpoints with untrusted certificates. <br>
Risk: Raw Docker API proxy operations may bypass normal operational guardrails. <br>
Mitigation: Add allowlists for permitted Docker API paths and methods before using the skill against production targets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Leventsoft/portainer-skill-openclaw) <br>
- [Portainer](https://www.portainer.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Portainer URL and API token.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
