## Description: <br>
Persistent structured memory system for OpenClaw agents with SQLite storage, hybrid search, rule-based capture, optional LLM-powered reflection, and adaptive trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oleglegegg](https://clawhub.ai/user/oleglegegg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Memory Oracle when an OpenClaw agent needs persistent cross-session memory, relevant context recall before responses, and structured preservation of critical instructions across compaction and restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain and reuse conversation or session data across agent runs. <br>
Mitigation: Use it only when persistent cross-session memory is intended, avoid storing secrets or regulated data, and periodically inspect and prune the SQLite database, MEMORY.md, and logs. <br>
Risk: Heavy-mode consolidation and reflection can send retained memory or daily logs to Anthropic. <br>
Mitigation: Leave ANTHROPIC_API_KEY unset and skip cron jobs unless external LLM processing is acceptable for the deployment. <br>
Risk: Reflected memories and guardrails can influence future agent behavior. <br>
Mitigation: Review reflected memories before allowing them to become durable guardrails or high-priority context. <br>


## Reference(s): <br>
- [Memory Oracle ClawHub page](https://clawhub.ai/oleglegegg/memory-oracle) <br>
- [README](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON memory/reflection artifacts, and text recall output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [SQLite-backed local memory; optional Anthropic API use for consolidation and reflection when ANTHROPIC_API_KEY is configured] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
