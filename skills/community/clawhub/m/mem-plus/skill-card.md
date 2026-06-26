## Description: <br>
Mem Plus provides identity-first, deterministic memory recall for a personal AI assistant with Chinese bigram boosting, credential filtering, deduplication, optional MMR reranking, and ChromaDB-backed memory commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars82311111](https://clawhub.ai/user/mars82311111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Mem Plus to search, wake, store, mine, and delete local personal or workspace memories for an AI assistant, especially when deterministic identity recall and Chinese-language matching are important. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, store, search, inject, and delete local memory or workspace data. <br>
Mitigation: Use it only with memory stores and workspace folders that are appropriate for agent access, and review ChromaDB stores periodically. <br>
Risk: Broad workspace mining may capture secrets or private files. <br>
Mitigation: Exclude sensitive paths before mining and avoid broad workspace scans unless private files and credentials have been removed or filtered. <br>
Risk: Stored memories may be injected into agent prompts and influence later responses. <br>
Mitigation: Review recalled context before relying on it for sensitive decisions and delete stale or inappropriate memories with the forget command. <br>


## Reference(s): <br>
- [Skill documentation](SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/mars82311111/mem-plus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May search, summarize, store, inject, or delete local memory and workspace data depending on the command used.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
