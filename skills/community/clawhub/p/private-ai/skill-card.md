## Description: <br>
Private AI helps agents set up and use local AI services for LLMs, image generation, speech-to-text, and embeddings on user-controlled hardware without cloud APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate local AI inference endpoints for private workloads, including chat, image generation, transcription, embeddings, monitoring, and air-gapped deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs the ollama-herd package as a local AI router. <br>
Mitigation: Verify the package source and version before installation, especially before processing sensitive data. <br>
Risk: The local service could be reachable beyond the intended network if binding or firewall settings are wrong. <br>
Mitigation: Confirm the service is bound and firewalled as intended before exposing local AI endpoints. <br>
Risk: Router logs under ~/.fleet-manager may contain operational metadata about requests and nodes. <br>
Mitigation: Review log contents and retention under ~/.fleet-manager before using the service with sensitive workloads. <br>
Risk: Model downloads and deletions affect local runtime state and storage. <br>
Mitigation: Require explicit user confirmation for model pulls and deletions, and do not delete or modify files in ~/.fleet-manager outside the documented workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/private-ai) <br>
- [Ollama Herd Repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash, Python, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local endpoint URLs and setup and monitoring commands; does not generate files directly.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
