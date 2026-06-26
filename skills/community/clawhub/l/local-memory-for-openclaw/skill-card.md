## Description: <br>
Local Memory stores and retrieves OpenClaw conversation memories on-device, automatically extracting key facts and injecting relevant context without external APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellofsf](https://clawhub.ai/user/hellofsf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to maintain local conversation memory across chats, including preferences, facts, project progress, and to-dos. It supports automatic memory extraction and injection plus manual commands for saving, recalling, listing, and deleting memories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation content may be automatically stored and reused across chats with limited user control. <br>
Mitigation: Review stored memories regularly, disable or modify automatic extraction and injection when inappropriate, and add opt-in or per-chat scoping before broad deployment. <br>
Risk: Sensitive information shared during conversations could be saved locally and later injected into unrelated context. <br>
Mitigation: Avoid sharing secrets or credentials while the skill is enabled, use the list and delete commands to audit stored content, and add filtering for sensitive values before storage. <br>
Risk: Similarity-based deletion can remove matching memories without a preview or confirmation step. <br>
Mitigation: Add a deletion preview and explicit confirmation flow before removing memories selected by semantic similarity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hellofsf/local-memory-for-openclaw) <br>
- [Skill usage documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSON event payloads with plain-text replies and injected memory context] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores memories locally in SQLite and uses local TF-IDF search; automatic extraction and injection are enabled by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
