## Description: <br>
Mnemo provides local file-system memory for OpenClaw, with Markdown storage, search, session auto-loading, and manual or threshold-based flush controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minmengxhw-cpu](https://clawhub.ai/user/minmengxhw-cpu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to give an agent persistent local memory, searchable recall, and daily or group-scoped Markdown journaling without a hosted database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent local memory and may retain sensitive conversation content in Markdown files. <br>
Mitigation: Use a private memoryDir, review stored Markdown files, and avoid saving secrets or regulated data unless the local environment is approved for that use. <br>
Risk: File-isolation guarantees need review according to the authoritative security summary. <br>
Mitigation: Avoid symlinks inside memoryDir, keep memoryDir permissions restrictive, and review path-handling behavior before deployment. <br>
Risk: The authoritative security guidance says the current flush function should not be treated as proof that session data was saved until fixed. <br>
Mitigation: Confirm important memories with explicit reads or file inspection after flush, and do not rely on flush alone for recovery-critical data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/minmengxhw-cpu/mnemo) <br>
- [Publisher profile](https://clawhub.ai/user/minmengxhw-cpu) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON tool results and Markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores persistent local Markdown under the configured memoryDir; semantic search uses local Ollama embeddings when enabled and falls back to keyword search.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
