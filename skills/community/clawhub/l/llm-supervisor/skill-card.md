## Description: <br>
Graceful rate limit handling with Ollama fallback that notifies on rate limits and offers a local model switch with confirmation for code tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhardie](https://clawhub.ai/user/dhardie) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to keep OpenClaw agents responsive when cloud LLM providers hit rate limits by switching to a local Ollama model while requiring confirmation before local code-generation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reroute agents between cloud and local LLM providers with unclear consent or persistence behavior. <br>
Mitigation: Review the configured cloud and local profiles before installing, define an explicit confirmationPhrase, and use /llm status after rate-limit events to confirm the active provider. <br>
Risk: Local LLM fallback may reduce code-generation quality in sensitive or production codebases. <br>
Mitigation: Keep confirmation required for local code tasks and proceed only after the user provides the configured confirmation phrase. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [ClawHub listing](https://clawhub.ai/dhardie/llm-supervisor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown command responses, user notifications, confirmation prompts, and LLM profile configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable localModel and confirmationPhrase values; default local model is qwen2.5:7b.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and skill.json; package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
