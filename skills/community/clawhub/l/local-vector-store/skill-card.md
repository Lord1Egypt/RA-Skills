## Description: <br>
Implements semantic search using local vector embeddings for knowledge base indexing and similarity matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackfeng0614-prog](https://clawhub.ai/user/jackfeng0614-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create a local, file-backed semantic search index for documents and retrieve matches by meaning rather than keyword overlap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local file write and delete behavior is loosely scoped to the configured store path. <br>
Mitigation: Review before installing, use only a dedicated private STORE_PATH, avoid untrusted document IDs, and avoid clear() on shared or important directories until scoped path validation is added. <br>
Risk: Indexed documents are persisted locally and may expose sensitive content if secrets or private data are indexed. <br>
Mitigation: Do not index secrets, restrict access to the store directory, and remove the dedicated store when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jackfeng0614-prog/local-vector-store) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Files] <br>
**Output Format:** [JSON-compatible JavaScript objects and local JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable VECTOR_DIMENSION, STORE_PATH, and SIMILARITY_THRESHOLD environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
