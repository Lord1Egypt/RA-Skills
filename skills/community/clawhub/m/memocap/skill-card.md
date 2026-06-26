## Description: <br>
忆时 is a local OpenCode memory capsule system that simulates human-like recall, stores long-term memories in ChromaDB, and supports active association and time capsules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenCode users use this skill to give an agent persistent local memory, retrieve prior context, manage time-capsule memories, and import or export memory archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic recall, storage, backup, and resurfacing of conversation details can expose or reintroduce sensitive personal context. <br>
Mitigation: Install only when persistent local memory is intended, review or disable the auto-loaded yishi-instructions, and require explicit confirmation before saving or recalling sensitive memories. <br>
Risk: Bulk import, export, and backup workflows can preserve or transfer private memory records outside the active ChromaDB store. <br>
Mitigation: Avoid importing sensitive files, protect exported Markdown and JSON files, protect the JSONL backup, and delete or encrypt exported memory artifacts when they are no longer needed. <br>
Risk: Aggressive automatic recall and storage can cause stale, misleading, or unwanted memories to influence later agent responses. <br>
Mitigation: Review recalled memories before relying on them and use update, delete, forget, or archive workflows to correct or retire stale records. <br>


## Reference(s): <br>
- [ChromaDB API reference](artifact/references/chroma-api.md) <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/memocap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI text, with optional JSON or Markdown export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, store, retrieve, archive, back up, import, and export local memory records depending on the configured OpenCode instructions and CLI command.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
