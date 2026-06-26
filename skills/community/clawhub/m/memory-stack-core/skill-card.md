## Description: <br>
Memory Stack Core provides a WAL, working buffer, and three-layer memory integration to preserve critical OpenClaw agent state across compaction and session restarts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neroagent](https://clawhub.ai/user/neroagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to persist important conversation details, recent exchanges, and memory health state across compaction or session restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save chat details and full exchanges into plaintext workspace files. <br>
Mitigation: Use it only when persistent local chat memory is intended, and avoid sessions containing secrets or regulated data. <br>
Risk: Persisted memory files may be committed to source control or copied into shared backups. <br>
Mitigation: Keep the memory directory out of git and shared backups, and periodically inspect or delete memory/wal.jsonl and memory/working-buffer.md. <br>
Risk: Automatic capture may store more conversation detail than the user expects. <br>
Mitigation: Disable auto_capture unless needed and review the generated memory files during operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neroagent/memory-stack-core) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/neroagent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration] <br>
**Output Format:** [JSON tool responses and local markdown or JSONL memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes plaintext memory artifacts under the workspace memory directory when capture tools are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
