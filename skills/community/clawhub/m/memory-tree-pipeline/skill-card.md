## Description: <br>
Three-scope structured memory for AI agents. Automatically organize, summarize, and index agent memory with sealing workers and topic extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larios613-hub](https://clawhub.ai/user/larios613-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain a local three-scope memory tree, migrate flat memory files, store and recall memories, seal raw source notes into topic summaries, and regenerate global knowledge files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently rewrite or delete local agent memory. <br>
Mitigation: Back up the memory workspace first, confirm the configured MEMORY_WORKSPACE and MEMORY_ROOT paths, use dry-run modes where available, and keep a separate recovery copy before using forget or source-deletion behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/larios613-hub/memory-tree-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Code] <br>
**Output Format:** [Markdown memory files, JSON indexes, Python module results, and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to a configurable local memory workspace and may update source, topic, global, and metadata files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
