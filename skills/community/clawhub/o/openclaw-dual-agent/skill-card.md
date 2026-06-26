## Description: <br>
Run two OpenClaw agents simultaneously: a paid Anthropic agent and a free agent using OpenRouter cloud models or local Ollama models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw with two isolated agents, separate Telegram bot routing, and either cloud or local model options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, Telegram bot tokens, and auth configuration files can expose sensitive credentials if copied into commands, logs, or shared files. <br>
Mitigation: Use dedicated provider keys and Telegram bots, restrict Telegram allowFrom to trusted chat IDs, authenticate interactively, redact logs, and keep auth-profiles.json and openclaw.json private with restrictive file permissions. <br>
Risk: The hybrid Ollama example can route prompts or context to OpenRouter cloud through fallback or heartbeat settings. <br>
Mitigation: Use the fully offline Ollama configuration when prompts or context must stay local by removing cloud fallbacks and pointing heartbeat to a local Ollama model. <br>
Risk: Incorrect Telegram bindings or reused account IDs can route messages to the wrong agent. <br>
Mitigation: Assign unique Telegram accountId values per binding, run openclaw doctor, and clean stale sessions before restart. <br>


## Reference(s): <br>
- [OpenClaw Dual Agent ClawHub Release](https://clawhub.ai/djc00p/openclaw-dual-agent) <br>
- [Configuration Reference](references/config-reference.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw, Telegram, OpenRouter, and Ollama configuration examples; users must substitute local paths and credentials.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
