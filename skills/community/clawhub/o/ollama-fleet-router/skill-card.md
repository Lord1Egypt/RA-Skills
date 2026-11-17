## Description:

Routes requests across multiple Ollama devices through one OpenAI-compatible endpoint with fleet scoring, auto-retry, VRAM-aware fallback, context protection, and support for chat, image generation, speech-to-text, and embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and operate an Ollama fleet router that presents one endpoint for model serving across multiple machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fleet nodes may receive prompts, files, audio, images, request metadata, and outputs routed to them.

Mitigation: Use only trusted fleet nodes and treat routed data as visible to the selected node.

Risk: Installing the Python package without review can introduce supply-chain exposure.

Mitigation: Install in an isolated Python environment or pin a reviewed package version.

Risk: Model downloads can consume significant bandwidth and disk space.

Mitigation: Require confirmation before pulling models and monitor storage on target nodes.

Risk: Operational commands can disrupt a running router or alter fleet state.

Mitigation: Keep confirmation guardrails for router and node restarts and for changes under ~/.fleet-manager/.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/twinsgeeks/skills/ollama-fleet-router)
- [Publisher profile](https://clawhub.ai/user/twinsgeeks)
- [ollama-herd package](https://pypi.org/project/ollama-herd/)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup commands, endpoint URLs, API examples, and operational guardrails.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
