## Description: <br>
Mac Mini AI helps developers set up a Mac Mini or Mac Mini fleet to run local LLMs, image generation, speech-to-text, embeddings, and OpenAI-compatible APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Apple Silicon Mac Minis as local AI nodes or small fleets for chat, image generation, speech-to-text, embeddings, and OpenAI-compatible application integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local AI service or fleet discovery endpoints may be reachable from other devices on the LAN if bound broadly. <br>
Mitigation: Run the service in an environment you control and confirm network binding, firewall, and LAN exposure before relying on it. <br>
Risk: The skill points users to install and run the referenced Ollama Herd package. <br>
Mitigation: Review the referenced package before installation and execute setup commands only after confirming they match the intended environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/twinsgeeks/mac-mini-ai) <br>
- [Ollama Herd GitHub project](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Ollama Herd PyPI package](https://pypi.org/project/ollama-herd/) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with shell, Python, and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local service endpoints and setup commands for user review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
