## Description:

Ollama Load Balancer helps agents guide deployment and operation of ollama-herd for load-balanced Ollama inference across multiple machines, including mDNS discovery, health checks, queue management, failover, and retry behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy and operate an Ollama load balancer, inspect fleet health, manage routing behavior, and troubleshoot local multi-node inference services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes package installation and local service commands for ollama-herd.

Mitigation: Install in a virtual environment, pin and review the ollama-herd package version before running it, and avoid elevated privileges.

Risk: Settings changes or model pull/delete actions can affect fleet behavior, disk usage, and network usage.

Mitigation: Require explicit user approval before changing settings or pulling or deleting models.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/ollama-load-balancer)
- [ollama-herd package](https://pypi.org/project/ollama-herd/)
- [ollama-herd repository](https://github.com/geeks-accelerator/ollama-herd)
- [Publisher profile](https://clawhub.ai/user/twinsgeeks)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash, Python, curl, and SQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local service URLs, operational checks, package installation commands, and confirmation-gated model management guidance.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
