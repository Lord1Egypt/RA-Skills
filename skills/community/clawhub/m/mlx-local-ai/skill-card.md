## Description: <br>
MLX Local AI helps agents guide setup and operation of local LLM, embedding, and OpenClaw gateway services on Apple Silicon Macs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saybanet](https://clawhub.ai/user/saybanet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, start, stop, check, and test local AI services on macOS Apple Silicon. It is intended for local chat-completions and embedding workflows exposed through OpenAI-compatible endpoints and an OpenClaw gateway configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run shell scripts that install unpinned Python packages and download model code on the user's Mac. <br>
Mitigation: Review the installation and startup scripts before execution, verify package and model sources, and install only in an isolated local environment. <br>
Risk: The startup workflow can run downloaded model code with trust-remote-code in a background service. <br>
Mitigation: Confirm that remote model code is acceptable for the environment, consider removing trust-remote-code, and monitor the local service logs. <br>
Risk: The embedding service depends on a local ~/embedding_server.py file whose contents may not be defined by the release artifact. <br>
Mitigation: Inspect ~/embedding_server.py before starting services and replace it with a reviewed implementation if needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/saybanet/mlx-local-ai) <br>
- [Publisher profile](https://clawhub.ai/user/saybanet) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup and service-management guidance for macOS Apple Silicon environments.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
