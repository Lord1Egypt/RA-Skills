## Description: <br>
Routes AI requests across free OpenRouter models for OpenClaw and Claude Code. Auto-discovers, scores, and configures the best free model with a smart fallback chain. Use when the user mentions free AI, OpenRouter, model switching, rate limits, or wants to reduce AI costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genoshide](https://clawhub.ai/user/genoshide) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to discover free OpenRouter chat models, choose a tool-capable primary model, and configure OpenClaw or Claude Code with fallbacks that reduce interruptions from rate limits or model failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use OpenRouter API keys and read keys from environment variables or local OpenClaw auth profiles. <br>
Mitigation: Use a dedicated OpenRouter key where possible and protect auth-profiles.json and OpenClaw configuration files. <br>
Risk: The skill can edit local OpenClaw or Claude Code model settings. <br>
Mitigation: Review the target configuration before and after running commands, and run validation mode before writing model selections when reliability matters. <br>
Risk: Watcher and daemon modes can automatically rotate models and restart OpenClaw after detected failures. <br>
Mitigation: Avoid watch, daemon, or notify modes unless automatic model rotation, gateway restarts, and optional webhook notifications are acceptable. <br>


## Reference(s): <br>
- [Infinity Router on ClawHub](https://clawhub.ai/genoshide/infinity-router) <br>
- [Publisher Profile](https://clawhub.ai/user/genoshide) <br>
- [OpenRouter Models API](https://openrouter.ai/api/v1/models) <br>
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions) <br>
- [OpenRouter Keys](https://openrouter.ai/keys) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local configuration changes for OpenClaw or Claude Code when commands are run.] <br>

## Skill Version(s): <br>
2.1.0 (source: pyproject.toml and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
