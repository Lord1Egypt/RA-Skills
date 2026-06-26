## Description: <br>
Control Docker containers and stacks via the Portainer API, including listing resources, starting, stopping, restarting, viewing logs, and redeploying stacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratiknarola](https://clawhub.ai/user/pratiknarola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and manage Portainer-backed Docker environments from shell commands. It is intended for container status checks, log review, stack redeploys, and controlled container lifecycle actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stop, restart, and redeploy Docker workloads through Portainer. <br>
Mitigation: Require explicit confirmation before stop, restart, or redeploy actions, especially for production environments. <br>
Risk: The Portainer API token is a sensitive credential. <br>
Mitigation: Use a least-privilege token, keep it out of repositories and logs, and restrict permissions on any environment file that stores it. <br>
Risk: TLS certificate validation is disabled in the API helper calls. <br>
Mitigation: Change the script to validate TLS certificates before using it with sensitive or production Portainer instances. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pratiknarola/portainer-docker) <br>
- [Publisher profile](https://clawhub.ai/user/pratiknarola) <br>
- [Portainer](https://portainer.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and command output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, PORTAINER_URL, and PORTAINER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
