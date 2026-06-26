## Description: <br>
Mac Studio AI helps agents set up and use Mac Studio systems for local LLM inference, image generation, speech-to-text, embeddings, and multi-device routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical operators use this skill to configure Mac Studio local AI workflows, connect client applications to a local router, add generation and transcription tools, and monitor a local AI fleet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup may expose a local or LAN AI router. <br>
Mitigation: Keep the service on a trusted network and review network exposure before use. <br>
Risk: Third-party Python packages are referenced for local AI workflows. <br>
Mitigation: Review the referenced packages before installation and use normal dependency controls. <br>
Risk: Operational logs and database files under ~/.fleet-manager may reveal local model or request activity. <br>
Mitigation: Treat ~/.fleet-manager data as operationally sensitive and limit access to trusted users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/mac-studio-ai) <br>
- [Ollama Herd project](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [Image Generation Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/image-generation.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python examples, curl API calls, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets macOS and references local or LAN services, optional Python tooling, and ~/.fleet-manager operational files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
