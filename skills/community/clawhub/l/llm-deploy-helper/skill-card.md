## Description: <br>
Detects local CPU, RAM, disk, and GPU capacity, recommends local LLM serving engines and models, and generates Docker Compose or systemd deployment files for Ollama, vLLM, and llama.cpp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to assess whether local hardware can run common LLM serving stacks and to produce starter deployment commands or configuration files. It is suited for local AI setup planning with Ollama, vLLM, and llama.cpp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Docker Compose and systemd files can expose local inference service ports, mount host volumes, and create services that restart or start on boot. <br>
Mitigation: Inspect generated files before running them, verify port and volume choices, and enable systemd services only when a persistent local LLM server is intended. <br>
Risk: vLLM configuration may include an optional Hugging Face token environment variable. <br>
Mitigation: Avoid passing tokens unless required for the selected model and keep token scope limited. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/minirr890112-byte/llm-deploy-helper) <br>
- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/llm-deploy-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style CLI guidance with generated Docker Compose YAML, systemd unit files, shell commands, and Rich terminal tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files may include exposed service ports, mounted model/cache volumes, GPU settings, and optional persistent service configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, pyproject.toml, package __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
