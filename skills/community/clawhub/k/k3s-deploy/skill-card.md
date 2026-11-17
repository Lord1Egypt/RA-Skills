## Description:

Automates deployment of K3s Kubernetes clusters across multiple Linux servers, including image pre-pulling, network interface detection, CNI setup, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuelin314-bot](https://clawhub.ai/user/xuelin314-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to deploy or repair multi-node K3s clusters on Linux servers, especially when they need scripted image pulling, network/CNI setup, and cluster readiness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact root SSH automation can reconfigure hosts and cluster networking.

Mitigation: Run only on intended hosts, verify target IPs and SSH host keys, and prepare rollback before deployment or repair commands.

Risk: Remote installers and container images are pulled during deployment.

Mitigation: Pin and verify K3s installers and container images before using the skill on real infrastructure.

Risk: Cluster credentials and SSH passwords may be exposed through command-line arguments or temporary files.

Mitigation: Prefer SSH keys over passwords, avoid command-line secrets, and secure or remove temporary token files after use.

## Reference(s):

- [K3s troubleshooting guide](references/troubleshooting.md)
- [K3s installer endpoint](https://get.k3s.io)
- [ClawHub skill page](https://clawhub.ai/xuelin314-bot/skills/k3s-deploy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and Kubernetes YAML/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create cluster summary and deployment log files during execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
