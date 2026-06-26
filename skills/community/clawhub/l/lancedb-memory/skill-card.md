## Description: <br>
Manage and retrieve long-term memories with LanceDB using local persistent storage, text or vector search helpers, categories, metadata, and agent-facing memory provider wrappers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pntrivedy](https://clawhub.ai/user/pntrivedy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add a local long-term memory store backed by LanceDB, then search, retrieve, update, delete, and summarize stored memories for an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored memories can persist sensitive or personal data on the local filesystem. <br>
Mitigation: Do not save secrets or sensitive personal data unless durable local retention is intended and approved for the deployment. <br>
Risk: The artifact uses a hard-coded local storage path for the LanceDB database. <br>
Mitigation: Verify or change the storage path before installation so memory data is written to an expected, access-controlled location. <br>
Risk: The skill depends on Python packages such as LanceDB, pandas, and PyArrow. <br>
Mitigation: Install dependencies from trusted package sources and review dependency policy before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pntrivedy/lancedb-memory) <br>
- [Publisher profile](https://clawhub.ai/user/pntrivedy) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance, text] <br>
**Output Format:** [Python modules with callable memory helpers and concise agent-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and queries a durable local LanceDB store; callers receive memory IDs, dictionaries, lists of records, and storage statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
