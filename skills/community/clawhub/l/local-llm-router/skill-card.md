## Description: <br>
Local LLM Router helps developers route OpenAI-compatible local LLM requests across multiple Ollama instances using scoring, context protection, VRAM-aware fallback, and retry behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, operate, inspect, and troubleshoot a self-hosted local LLM routing service across macOS, Linux, and Windows machines running Ollama. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing an unverified package could introduce unwanted code into the local environment. <br>
Mitigation: Verify the `ollama-herd` PyPI package and repository before running installation commands. <br>
Risk: The local dashboard and API expose fleet status, traces, settings, and model management endpoints. <br>
Mitigation: Keep the localhost dashboard and API private and avoid exposing them beyond the intended local network. <br>
Risk: Pulling or deleting local LLM models can consume substantial storage or remove needed models. <br>
Mitigation: Require explicit user confirmation before pull or delete actions. <br>
Risk: Router logs and latency databases may contain operational history needed for troubleshooting. <br>
Mitigation: Do not delete or modify files under `~/.fleet-manager/` unless the user explicitly requests that change. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/local-llm-router) <br>
- [ollama-herd Repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [ollama-herd PyPI Package](https://pypi.org/project/ollama-herd/) <br>
- [Twin Geeks Publisher Profile](https://clawhub.ai/user/twinsgeeks) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local service endpoints, operational checks, SQL inspection commands, and guardrails for model and router management.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
