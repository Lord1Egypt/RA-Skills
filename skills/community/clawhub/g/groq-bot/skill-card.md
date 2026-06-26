## Description: <br>
Fast, low-latency text generation using Groq free-tier models for summaries, reasoning, trading analysis, and tool-assisted responses with automatic fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silaskade](https://clawhub.ai/user/silaskade) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route short to medium text-generation tasks through Groq models with rate-limit handling, model fallback, and optional tool-assisted responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Groq credentials and includes API-key-like configuration evidence. <br>
Mitigation: Provide a fresh Groq key through a secret or environment variable, remove bundled key-like values before use, and avoid exposing credentials in logs or outputs. <br>
Risk: Conversation history and memory files may persist and be resent in later model requests. <br>
Mitigation: Review or clear bundled memory and conversation files before use, and disable or limit persistence when handling private or shared-context data. <br>
Risk: Bundled agent instructions include broad autonomous heartbeat, memory-maintenance, and commit/push behaviors beyond simple Groq text generation. <br>
Mitigation: Review or remove AGENTS.md, HEARTBEAT.md, and start_bot.sh behaviors unless proactive background work and shell-driven session spawning are explicitly intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/silaskade/groq-bot) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/silaskade) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown responses, with code blocks or shell commands when the agent task calls for them.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be constrained by Groq model limits, configured token caps, rate-limit handling, and conversation-history trimming.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
