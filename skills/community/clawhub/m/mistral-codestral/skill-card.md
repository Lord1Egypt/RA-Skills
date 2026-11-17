## Description:

Mistral Codestral helps agents set up and use a local Ollama Herd fleet for Mistral Large, Mistral-Nemo, Codestral, Mistral-Small, and related local inference endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and operate a local Mistral-compatible Ollama Herd router, run code-generation and reasoning prompts, and monitor local fleet status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance installs the unpinned `ollama-herd` Python package, which can reduce reproducibility across environments.

Mitigation: Install in a virtual environment and pin or review the package version before use in controlled deployments.

Risk: Local prompts, generated files, uploaded audio, and model activity are handled by the user's local fleet service.

Mitigation: Treat those inputs and outputs as local service data and apply the same data-handling controls used for other local inference workloads.

Risk: Mistral model downloads can be large and model deletion affects local assets.

Mitigation: Require explicit user confirmation before model downloads or deletion, and do not delete or modify files under `~/.fleet-manager/`.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/mistral-codestral)
- [Ollama Herd Repository](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash, Python, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes local endpoint examples, hardware recommendations, monitoring commands, and guardrails for model downloads and local fleet files.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
