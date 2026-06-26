## Description: <br>
Ollama Ollama Herd routes requests across a local Ollama fleet through one OpenAI-compatible endpoint, with model scoring, retry, VRAM-aware fallback, image generation, speech-to-text, and embeddings support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure and use a self-hosted Ollama fleet router that selects available local nodes for chat, embeddings, image generation, and speech-to-text workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The auto-pull behavior may download models and change local Ollama node state, using bandwidth, disk, or VRAM unexpectedly. <br>
Mitigation: Review the ollama-herd package and repository before installing, prefer an isolated environment where practical, and confirm auto-pull behavior before allowing model downloads across nodes. <br>
Risk: Router or node management commands can affect local fleet availability and data under ~/.fleet-manager/. <br>
Mitigation: Get user confirmation before restarting router or node agents, deleting local fleet data, or pulling or deleting Ollama models. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/ollama-ollama-herd) <br>
- [ollama-herd package](https://pypi.org/project/ollama-herd/) <br>
- [Ollama Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers macOS, Linux, and Windows environments and references local Ollama router configuration paths.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
