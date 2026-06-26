## Description: <br>
Persistent memory plugin for OpenClaw agents. Hybrid SQLite FTS5 keyword + Ollama vector semantic search with auto-capture, auto-recall, stuck-detection, and memory consolidation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinodell](https://clawhub.ai/user/kevinodell) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this plugin to give agents durable memory across session resets, compaction, and restarts. It supports automatic recall, automatic fact capture, keyword and semantic search, entity lookup, manual memory storage, and repetition detection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory and automatic recall can carry stored facts into future prompts. <br>
Mitigation: Install only when durable agent memory is intended, review stored memory data regularly, and disable autoRecall for workflows where previous context should not be injected. <br>
Risk: Startup session health behavior can alter OpenClaw session files. <br>
Mitigation: Review the session auto-reset behavior before enabling the plugin and keep backups or test in a disposable profile before using it with important sessions. <br>
Risk: Automatic capture can store sensitive or unwanted facts from conversations. <br>
Mitigation: Disable autoCapture for sensitive work or use stricter capture settings such as assistant-only or tagged capture where supported. <br>
Risk: Vector search sends text to the configured Ollama embedding endpoint. <br>
Mitigation: Keep Ollama pointed at a trusted local endpoint or disable vectorSearch when semantic recall is not required. <br>


## Reference(s): <br>
- [ClawHub Lily Memory Plugin](https://clawhub.ai/kevinodell/lily-memory) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [OpenClaw Plugin Manifest](artifact/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Text and Markdown tool results, injected context blocks, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Memory recall is bounded by configured result and context budgets; semantic search depends on a trusted local Ollama endpoint when vectorSearch is enabled.] <br>

## Skill Version(s): <br>
5.2.3 (source: server release metadata, package.json, openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
