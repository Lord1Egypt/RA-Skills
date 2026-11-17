## Description:

Manage multi-tier AI inference clusters for homelabs with health monitoring, expert MoE routing, automatic node recovery, model deployment across Ollama and llama.cpp nodes, GPU memory planning, Docker volume patterns, sequential startup guidance, and LiteLLM gateway configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlesnews](https://clawhub.ai/user/mlesnews)

### License/Terms of Use:

MIT

## Use Case:

Developers and homelab operators use this skill to monitor, route, recover, and deploy heterogeneous local AI inference clusters across GPU, CPU, Ollama, llama.cpp, and LiteLLM components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic remote recovery can restart Docker services or open SSH/RDP recovery paths on hosts.

Mitigation: Use the skill only on homelab hosts you control and require explicit approval before SSH/RDP recovery or Docker restarts.

Risk: Mutable Docker image references and broad model mounts can change runtime behavior or expose more host data than intended.

Mitigation: Pin Docker images by digest and mount source model paths read-only and narrowly.

Risk: Recovery credentials could be exposed if stored or passed insecurely.

Mitigation: Keep recovery credentials in a vault and pass secrets through stdin rather than command-line arguments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mlesnews/skills/homelab-cluster)
- [Lumina Homelab](https://luminahomelab.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational patterns for endpoint health checks, Docker deployment, sequential restarts, recovery workflows, GPU memory planning, and LiteLLM routing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
