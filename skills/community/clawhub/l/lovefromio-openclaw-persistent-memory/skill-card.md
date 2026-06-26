## Description: <br>
Persistent memory system - automatic context capture and semantic search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovefromio](https://clawhub.ai/user/lovefromio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add long-term agent memory with automatic context capture, semantic search, and recall across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses long-term agent context, which can include sensitive or outdated information. <br>
Mitigation: Use it only when persistent memory is intended, avoid storing secrets, and review or back up the memory database before deleting or relying on stored memories. <br>
Risk: Automatic capture and recall can inject stored context into later prompts without the user noticing every retrieved item. <br>
Mitigation: Consider disabling autoCapture or autoRecall until the team understands what is stored and when memories are recalled. <br>
Risk: The installation documentation includes both reviewed package installation and a curl-to-bash path. <br>
Mitigation: Prefer ClawHub or reviewed npm installation, inspect scripts before execution, and keep the memory worker bound to localhost. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lovefromio/lovefromio-openclaw-persistent-memory) <br>
- [Installation Guide](INSTALL.md) <br>
- [Full Documentation](SKILL.md) <br>
- [npm Package](https://www.npmjs.com/package/openclaw-persistent-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local worker setup, OpenClaw extension configuration, and memory search guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
