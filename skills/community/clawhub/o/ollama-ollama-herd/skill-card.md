## Description:

Ollama Ollama Herd helps agents set up and use Ollama Herd as a self-hosted multimodal router that exposes one OpenAI-compatible Ollama endpoint across macOS, Linux, and Windows devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install Ollama Herd, route local Ollama chat, embeddings, image, and speech-to-text requests through one fleet endpoint, and apply the stated guardrails before changing router state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supply-chain exposure from installing and running the ollama-herd package.

Mitigation: Install in an isolated environment or trusted fleet and pin or review the package before use.

Risk: Prompts, audio, logs, and auto-pulled models may move through local fleet components or be stored in local router paths.

Mitigation: Confirm storage and routing behavior before using sensitive data, and review the configured fleet-manager paths.

Risk: Router, node, or model-management actions can change host state.

Mitigation: Avoid elevated privileges and require user confirmation before restarting services, pulling models, deleting models, or modifying fleet-manager data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/ollama-ollama-herd)
- [Ollama Herd package](https://pypi.org/project/ollama-herd/)
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd)
- [Ollama Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash, Python, and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local endpoints, fleet-manager state paths, and optional Python or sqlite tooling.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact frontmatter says 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
