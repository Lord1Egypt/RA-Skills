## Description: <br>
Enhances OpenClaw memory by automatically recalling relevant past workspace memories before each turn and capturing durable conversation details after agent runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoulf1006](https://clawhub.ai/user/zhoulf1006) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this plugin to provide agents with persistent workspace context by recalling relevant memories and capturing durable facts, preferences, and decisions from recent conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent conversations may be summarized into persistent workspace memory and reused in later prompts. <br>
Mitigation: Disable autoCapture for sensitive work, avoid entering secrets or regulated data while enabled, and regularly review stored memory files. <br>
Risk: Automatically recalled memories may include stale or untrusted historical context. <br>
Mitigation: Keep autoRecall disabled when strict context isolation is required and review recalled memory content before relying on it for decisions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/zhoulf1006/memory-core-plus) <br>
- [Publisher profile](https://clawhub.ai/user/zhoulf1006) <br>
- [README](artifact/README.md) <br>
- [Plugin manifest](artifact/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Prompt context text plus Markdown memory entries and JSON-style configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Auto-recall injects up to the configured maximum number of relevant memories per turn; auto-capture analyzes up to the configured maximum number of recent messages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
