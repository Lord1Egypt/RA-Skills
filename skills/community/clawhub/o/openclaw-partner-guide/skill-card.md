## Description: <br>
Partner-style operating guide for OpenClaw assistants. Use when an assistant should behave like a proactive, careful partner rather than a generic chatbot, with strong defaults for concise communication, memory hygiene, phased execution, skill vetting, shared-chat restraint, and cautious external actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javvvid](https://clawhub.ai/user/javvvid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and assistant operators use this skill to give OpenClaw assistants a concise, proactive operating style for communication, memory hygiene, phased work, safe skill review, and restrained shared-chat behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages memory, daily logs, and scheduled follow-ups, which can retain user preferences or operational context longer than expected. <br>
Mitigation: Keep memory and scheduled continuations scoped to the user's preferences, and review or clear stored memory when needed. <br>
Risk: The guide can make an assistant more proactive, including during long tasks and delayed follow-through. <br>
Mitigation: Ask before risky, destructive, outbound, or external actions, and keep follow-up behavior tied to a clearly stated goal and retry time. <br>


## Reference(s): <br>
- [OpenClaw Partner Guide](https://clawhub.ai/javvvid/openclaw-partner-guide) <br>
- [Execution Patterns](references/execution-patterns.md) <br>
- [Memory Patterns](references/memory-patterns.md) <br>
- [Shared Chat Patterns](references/shared-chat-patterns.md) <br>
- [Skill Safety](references/skill-safety.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text, shell commands] <br>
**Output Format:** [Markdown guidance with optional plain-text helper-script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides assistant behavior and includes small local helper scripts for partner summaries and handoff summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
