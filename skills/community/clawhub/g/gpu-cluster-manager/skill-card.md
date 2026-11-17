## Description:

GPU Cluster Manager helps agents set up and operate a local AI GPU cluster that runs Llama, Qwen, DeepSeek, and Phi across macOS, Linux, and Windows devices through one endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure, inspect, and manage a self-hosted Ollama GPU cluster for local LLM inference. It guides routing, node startup, health checks, dashboard use, model management, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running the package with broad privileges can increase local system exposure.

Mitigation: Install it in a dedicated environment, avoid elevated privileges, and review the PyPI or GitHub package before use.

Risk: Pulling or deleting models can consume or remove significant storage, bandwidth, and GPU resources.

Mitigation: Require explicit confirmation before model pull or delete actions and keep auto-pull settings under user control.

Risk: Exposing the cluster endpoint beyond trusted machines can make local inference resources available to unintended clients.

Mitigation: Restrict the cluster endpoint to trusted machines and networks.

Risk: Changing files under ~/.fleet-manager/ can affect cluster data, logs, and learned routing state.

Mitigation: Do not delete or modify ~/.fleet-manager/ contents unless the user explicitly asks and understands the impact.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/gpu-cluster-manager)
- [Project Homepage](https://github.com/geeks-accelerator/ollama-herd)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with shell commands, code snippets, URLs, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent guidance may include local endpoint checks, package installation commands, model-management requests, and configuration paths.]

## Skill Version(s):

1.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
