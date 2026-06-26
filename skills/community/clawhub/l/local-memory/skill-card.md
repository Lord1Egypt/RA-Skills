## Description: <br>
Local Memory stores, searches, and deletes persistent local semantic memories using ChromaDB and the BGE-small-zh embedding model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangmu-git2](https://clawhub.ai/user/liangmu-git2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain an offline long-term memory store, recall prior facts or preferences by semantic search, and remove stored memories when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup downloads Python packages and an embedding model before first use. <br>
Mitigation: Install in an isolated Python environment and review the dependency and model download behavior before running setup. <br>
Risk: Memory text persists on disk in the skill's local data directory. <br>
Mitigation: Do not store secrets or highly sensitive information unless persistent local storage is acceptable. <br>
Risk: Query-based deletion removes the single best semantic match, which may not be the exact intended record. <br>
Mitigation: Use recall to inspect matching records and prefer ID-based deletion when exact removal matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liangmu-git2/local-memory) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses from local Python scripts, with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores memory records persistently in the skill's local data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
