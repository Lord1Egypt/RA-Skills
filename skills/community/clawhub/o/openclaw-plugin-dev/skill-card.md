## Description: <br>
Guides developers through creating OpenClaw plugins with lifecycle hooks, request-response correlation, logging, configuration, and debugging patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cicadafang](https://clawhub.ai/user/cicadafang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to draft and reason about OpenClaw plugin structure, hook registration, logging, configuration, and debugging workflows. It is most useful when building plugins that inspect LLM input/output events or manage per-session plugin state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logging examples can expose prompts, system prompts, chat history, or model outputs if copied without safeguards. <br>
Mitigation: Make conversation logging opt-in, redact sensitive fields, restrict log file permissions, and define retention or deletion behavior before deployment. <br>
Risk: Plugins that depend on normal session termination can miss llm_output events during interruptions, leaving incomplete request-response correlation or cleanup. <br>
Mitigation: Design handlers to tolerate missing output events, expire in-flight state, and clean up resources on agent_end or equivalent lifecycle boundaries. <br>


## Reference(s): <br>
- [Openclaw Plugin Dev on ClawHub](https://clawhub.ai/cicadafang/openclaw-plugin-dev) <br>
- [Example LLM API Logger Plugin](https://github.com/cicadaFang/openclaw-llm-api-logger) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no tools or external services are invoked by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
