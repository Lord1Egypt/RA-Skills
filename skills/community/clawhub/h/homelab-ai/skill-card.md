## Description: <br>
Home lab AI turns spare macOS, Linux, and Windows machines into a local AI cluster for LLM inference, image generation, speech-to-text, and embeddings with mDNS discovery, a dashboard, and local routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, home-lab operators, and agent builders use this skill to set up and operate an Ollama Herd local AI router across trusted personal or lab machines. It provides installation commands, API examples, model guidance, dashboard usage, and guardrails for local inference workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package installation commands can introduce supply-chain risk if packages are not reviewed before use. <br>
Mitigation: Verify the PyPI and uv packages before installing or running them. <br>
Risk: The local AI endpoint can expose prompts, documents, audio, or generated outputs if reachable from untrusted networks. <br>
Mitigation: Run the router only on trusted machines and a trusted LAN; avoid exposing the endpoint to untrusted networks. <br>
Risk: Fleet logs and routing data under ~/.fleet-manager may contain sensitive local usage details. <br>
Mitigation: Review log contents before sharing prompts, audio, documents, or diagnostics from the cluster. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/homelab-ai) <br>
- [Ollama Herd homepage](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [Image Generation Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/image-generation.md) <br>
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md) <br>
- [Troubleshooting](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with bash, Python, curl, URL, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local endpoint examples, dashboard URL, model recommendations, and home-lab guardrails.] <br>

## Skill Version(s): <br>
1.0.2 (source: target metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
