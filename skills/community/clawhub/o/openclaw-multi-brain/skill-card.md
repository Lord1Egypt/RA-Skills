## Description: <br>
Runs additional LLM perspectives before an OpenClaw agent response and injects those perspectives into the agent context for synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dannydvm](https://clawhub.ai/user/Dannydvm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add a second or third model perspective before an agent answers, typically to surface alternative angles, risks, and verification prompts during agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hook or daemon can read local agent conversations and memory/context content, then send selected content to configured AI providers. <br>
Mitigation: Use local Ollama for sensitive work, set ownerIds to limit whose sessions are processed, and review any context file or MEMORY.md content before enabling the skill. <br>
Risk: The skill can run persistently as a service or hook and continue monitoring session files. <br>
Mitigation: Install it only in trusted workspaces, verify daemon status and logs, and disable or uninstall the service when it is not needed. <br>
Risk: API keys may be stored in plaintext configuration or local key files. <br>
Mitigation: Avoid production API keys, restrict file permissions, rotate keys after testing, and prefer providers that do not require external credentials when possible. <br>
Risk: Injected perspectives may be hidden from the end user or make the final answer appear to come from a single model. <br>
Mitigation: Remove instructions that hide provenance before shared or regulated use, and disclose when external model perspectives are part of the agent workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Dannydvm/openclaw-multi-brain) <br>
- [Publisher profile](https://clawhub.ai/user/Dannydvm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown perspective content, hook-injected context, and CLI-oriented setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write latest-perspective files and can call configured local or remote LLM providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
