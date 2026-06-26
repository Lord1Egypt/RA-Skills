## Description: <br>
Manage Hetzner Cloud infrastructure using the hcloud CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpj069](https://clawhub.ai/user/jpj069) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to manage Hetzner Cloud servers, firewalls, SSH keys, volumes, networks, load balancers, and related CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through powerful Hetzner Cloud actions, including deletion or production-impacting infrastructure changes. <br>
Mitigation: Require explicit confirmation before delete, rebuild, stop, firewall, or other production-impacting commands. <br>
Risk: The skill uses a Hetzner Cloud API token stored in the hcloud configuration file. <br>
Mitigation: Use a narrowly scoped API token where possible and protect the hcloud configuration file with restrictive permissions. <br>


## Reference(s): <br>
- [Hetzner Cloud Documentation](https://docs.hetzner.cloud/) <br>
- [Hetzner Cloud CLI GitHub Repository](https://github.com/hetznercloud/cli) <br>
- [ClawHub Skill Page](https://clawhub.ai/jpj069/hcloud) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
