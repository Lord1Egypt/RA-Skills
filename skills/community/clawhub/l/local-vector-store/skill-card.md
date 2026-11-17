## Description:

Implements semantic search using local vector embeddings for knowledge base indexing and similarity matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackfeng0614-prog](https://clawhub.ai/user/jackfeng0614-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to maintain a local searchable document index and retrieve documents by similarity without calling external APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted document IDs could write or delete JSON files outside the configured storage folder.

Mitigation: Use only trusted document IDs, run the skill with an isolated STORE_PATH, and limit filesystem permissions until path validation is fixed.

Risk: Search behavior may be misleading because the embedding implementation is not a true semantic embedding model.

Mitigation: Do not rely on results for true semantic search unless the embedding implementation is replaced and validated for the intended corpus.

Risk: Indexed content may persist locally with unclear deletion behavior.

Mitigation: Avoid indexing sensitive documents until persistence and deletion behavior are documented and verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackfeng0614-prog/skills/local-vector-store)

## Skill Output:

**Output Type(s):** [code, JSON, configuration]

**Output Format:** [JavaScript API calls returning JSON-like objects for indexing, search results, deletion, and store statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local filesystem storage configured by VECTOR_DIMENSION, STORE_PATH, and SIMILARITY_THRESHOLD.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
