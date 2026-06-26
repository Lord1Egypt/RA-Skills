## Description: <br>
A Proxmox-native orchestration skill that turns any home lab into a Self-Healing AI Swarm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spamtylor](https://clawhub.ai/user/spamtylor) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and home-lab operators use Hydra Evolver to scan known mesh nodes, provision OpenClaw-related host dependencies, and generate JSON resume plans from project and memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install system software and change host networking state. <br>
Mitigation: Review scripts before execution and do not allow mesh_provision to run automatically. <br>
Risk: The skill can scan local machines on a predefined private subnet. <br>
Mitigation: Restrict scanning to hosts and networks you own or administer. <br>
Risk: Proxmox access may expose infrastructure control if credentials are overprivileged. <br>
Mitigation: Use least-privilege Proxmox tokens and protect PVE_TOKEN_ID and PVE_TOKEN_SECRET. <br>
Risk: The hardening claim is not verified by the available evidence. <br>
Mitigation: Treat hardening claims as unverified until the scripts and runtime behavior are reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spamtylor/hydra-evolver) <br>
- [Docker install script](https://get.docker.com) <br>
- [Volta installer](https://get.volta.sh) <br>
- [Tailscale install script](https://tailscale.com/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands, command output, and JSON plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce an evolution_plan.json-style action plan and local mesh scan results.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
