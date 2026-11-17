## Description:

MLX-powered local AI for running LLMs, Stable Diffusion, speech-to-text, and embeddings natively on Apple Silicon via MLX, coordinated by an Ollama Herd fleet router across Mac devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up and operate a local Apple Silicon AI fleet for LLM inference, image generation, speech-to-text, and embeddings through MLX-backed tools. It provides installation commands, local API examples, monitoring endpoints, and operational guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installation can introduce ordinary supply-chain or environment risks.

Mitigation: Install Python tools in an isolated environment, avoid sudo, and pin reviewed versions of ollama-herd, mflux, and diffusionkit where practical.

Risk: Prompts, audio files, embeddings, and generated content are routed to local fleet nodes.

Mitigation: Treat data sent to the local router as available to those nodes and restrict the fleet to trusted machines and networks.

Risk: Model downloads and deletion operations can affect local storage and model availability.

Mitigation: Keep explicit user confirmation for model pulls and deletion, and do not delete or modify files under ~/.fleet-manager/.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/mlx-apple-silicon-mlx)
- [MLX Framework](https://github.com/ml-explore/mlx)
- [Ollama Herd](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [Image Generation Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/image-generation.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)
- [Ollama Herd on PyPI](https://pypi.org/project/ollama-herd/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline bash, Python, and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets macOS on Apple Silicon and references local services on port 11435.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
