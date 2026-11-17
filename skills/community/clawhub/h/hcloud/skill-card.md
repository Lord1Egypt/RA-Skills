## Description:

Manage Hetzner Cloud infrastructure with the hcloud CLI, including servers, firewalls, SSH keys, volumes, networks, load balancers, and infrastructure monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpj069](https://clawhub.ai/user/jpj069)

### License/Terms of Use:


## Use Case:

Developers and infrastructure operators use this skill to get hcloud CLI guidance for managing Hetzner Cloud servers, firewalls, SSH keys, volumes, networks, and load balancers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact Hetzner Cloud administration actions such as creating, stopping, deleting, and remotely accessing cloud resources.

Mitigation: Require explicit approval before stop, delete, and remote-shell actions, and review generated commands before execution.

Risk: The skill includes a risky system-wide hcloud CLI install path.

Mitigation: Prefer a pinned, verified hcloud release installed in a user-owned path.

Risk: Broad cloud credentials or public SSH firewall rules can expand the blast radius of mistakes.

Mitigation: Use least-privilege or project-scoped Hetzner tokens and avoid broad public SSH rules unless explicitly required.

## Reference(s):

- [Hetzner Cloud Documentation](https://docs.hetzner.cloud/)
- [Hetzner Cloud CLI](https://github.com/hetznercloud/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational command sequences for cloud resource administration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
