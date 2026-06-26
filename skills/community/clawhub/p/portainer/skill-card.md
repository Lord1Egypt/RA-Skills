## Description: <br>
Control Docker containers and stacks via Portainer API. List containers, start/stop/restart, view logs, and redeploy stacks from git. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asteinberger](https://clawhub.ai/user/asteinberger) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect Portainer environments, manage Docker containers, view logs, and redeploy stacks through the Portainer API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stop, restart, and redeploy live services through Portainer. <br>
Mitigation: Use a least-privilege Portainer API key, scope access to non-production where possible, and require explicit confirmation before stop, restart, or redeploy actions. <br>
Risk: Portainer API credentials can grant infrastructure control if exposed. <br>
Mitigation: Store PORTAINER_API_KEY securely, rotate it if exposed, and avoid embedding it in prompts or shared logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/asteinberger/portainer) <br>
- [Publisher Profile](https://clawhub.ai/user/asteinberger) <br>
- [Portainer](https://portainer.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, API calls] <br>
**Output Format:** [Markdown guidance with bash commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PORTAINER_URL, PORTAINER_API_KEY, curl, and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
