## Description: <br>
Hongnao Memory V1.0.0 provides long-term memory management for OpenClaw with cross-session persistence, intelligent retrieval, and preference learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangfengxm](https://clawhub.ai/user/tangfengxm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add local long-term memory, retrieve prior context across sessions, and learn user preferences from conversation-derived data. It is most relevant for agents that need persistent personalization and memory search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory capture can store conversation-derived facts, preferences, and possibly full session messages. <br>
Mitigation: Require explicit user opt-in, define what may be stored, and disable automatic extraction or session sync when persistent memory is not needed. <br>
Risk: Stored memories may include secrets, regulated data, or sensitive personal information. <br>
Mitigation: Avoid storing secrets or regulated data, review memory contents before persistence, and protect the local workspace from syncing or sharing. <br>
Risk: Forgetting, deletion, and memory updates can remove or alter important context. <br>
Mitigation: Create a backup and recovery plan before enabling cleanup, forgetting, or deletion workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangfengxm/hongnao-memory-v1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/tangfengxm) <br>
- [README.md](artifact/README.md) <br>
- [RELEASE_NOTES.md](artifact/RELEASE_NOTES.md) <br>
- [Integration guide](artifact/集成指南.md) <br>
- [Quick start](artifact/快速入门.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, configuration examples, and JSON-like memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and retrieves local memory content, including conversation-derived facts and preferences, according to the configured OpenClaw integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release.version, artifact manifest.json, artifact plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
