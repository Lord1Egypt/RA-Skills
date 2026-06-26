## Description: <br>
Mempalace Memory retrieves and manages persistent local memories for an agent using MemPalace with optional SuperMem/ChromaDB synchronization, deduplication, metadata cleanup, and reranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars82311111](https://clawhub.ai/user/mars82311111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add local long-term memory recall to an OpenClaw-style agent, including search, wake-up context, manual memory storage, memory mining, and deletion commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can mine workspace content into persistent local memory stores and later inject recalled content into agent prompts. <br>
Mitigation: Run mining only on explicitly approved directories and avoid storing secrets or private material in memory stores. <br>
Risk: Bridge and forget commands can synchronize, modify, or delete local MemPalace and ChromaDB memory data. <br>
Mitigation: Back up memory stores before running bridge or forget commands and test changes on noncritical data first. <br>
Risk: The artifact references hard-coded user-specific paths and a hook handler that is not included in the submitted files. <br>
Mitigation: Verify and adapt the hook handler and CLI paths before installation or automated use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mars82311111/mempalace-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses from CLI scripts plus Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can persist, retrieve, synchronize, or delete local memory stores under user-specific paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
