## Description: <br>
Ollama fleet router - herd your Ollama LLMs into one smart endpoint, route common Ollama models across multiple devices with 7-signal scoring, auto-retry, VRAM-aware fallback, context protection, image generation, speech-to-text, embeddings, and drop-in OpenAI SDK compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate an Ollama fleet router that exposes one smart endpoint across multiple local Ollama devices. It helps route chat, embeddings, image generation, and speech-to-text requests while showing safe operational guardrails for router, node, and model changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fleet nodes may receive prompts, files, audio, and metadata routed through the shared endpoint. <br>
Mitigation: Install only when every fleet node is trusted, keep the router on trusted networks, and review upstream package behavior before use. <br>
Risk: Router or model operations can trigger large downloads or remote node state changes. <br>
Mitigation: Use pinned package versions where practical and require confirmation before model pulls, model deletion, router restarts, or node-agent changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/ollama-fleet-router) <br>
- [ollama-herd package](https://pypi.org/project/ollama-herd/) <br>
- [ollama-herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes guardrails for confirmation before router restarts, node-agent changes, fleet-manager file changes, and model pulls or deletions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
