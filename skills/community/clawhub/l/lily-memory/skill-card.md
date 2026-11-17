## Description:

Persistent memory plugin for OpenClaw agents with hybrid SQLite FTS5 keyword and Ollama vector semantic search, auto-capture, auto-recall, stuck detection, and memory consolidation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinodell](https://clawhub.ai/user/kevinodell)

### License/Terms of Use:

MIT

## Use Case:

External developers and OpenClaw operators use this plugin to give agents persistent local memory across resets, compaction, and restarts. It supports memory search, fact storage, semantic recall, entity lookup, and repetition nudges during agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin stores and re-injects persistent conversation memory by default, which can expose sensitive or outdated context to later turns.

Mitigation: Use it only where persistent local memory is acceptable, set capturePolicy to assistant-only or tagged-only, and disable autoCapture or autoRecall for sensitive workflows.

Risk: Vector search can send captured memory text to the configured Ollama endpoint.

Mitigation: Keep ollamaUrl on a trusted local endpoint or disable vectorSearch when memory text should not leave the local host.

Risk: The session health guard can automatically reset OpenClaw sessions when it detects context overflow.

Mitigation: Install only if automatic session reset behavior is acceptable, or patch or disable the guard before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kevinodell/skills/lily-memory)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [OpenClaw Plugin Manifest](openclaw.plugin.json)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and text tool responses, configuration snippets, and injected context blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include recalled local memories, search results, stored fact confirmations, security log summaries, and repetition nudges.]

## Skill Version(s):

5.2.3 (source: server release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
