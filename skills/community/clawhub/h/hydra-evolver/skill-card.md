## Description:

A Proxmox-native orchestration skill that turns any home lab into a Self-Healing AI Swarm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spamtylor](https://clawhub.ai/user/spamtylor)

### License/Terms of Use:

MIT

## Use Case:

Developers and home-lab operators use this skill to discover mesh nodes, provision new hardware with OpenClaw dependencies, and generate resume plans for paused work from local project files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provisioning workflow can make broad system and network changes, including Docker installation, Docker group access, Node.js installation, Tailscale installation, and a global OpenClaw install.

Mitigation: Run provisioning only on machines you control after reviewing remote installers, pinning package versions where possible, and deciding whether Docker group access and Tailscale are acceptable.

Risk: The mesh scan probes LAN hosts and can be interpreted as network scanning.

Mitigation: Run scans only on approved networks and restrict configured target IP ranges to authorized hosts.

Risk: The evolution workflow generates resume actions from local project and memory files that may be incomplete or misleading.

Mitigation: Review generated plans before applying them or using them to change code, infrastructure, or project state.

## Reference(s):

- [Hydra Evolver on ClawHub](https://clawhub.ai/spamtylor/skills/hydra-evolver)
- [Docker installer endpoint used by provision.sh](https://get.docker.com)
- [Volta installer endpoint used by provision.sh](https://get.volta.sh)
- [Tailscale installer endpoint used by provision.sh](https://tailscale.com/install.sh)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON plans and scan results, plus shell command output from provisioning workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect local PROJECTS.md and MEMORY.md files and probe configured LAN IP addresses when invoked.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
