## Description:

Ingests external knowledge-base documents, notes, and shared files into vector databases such as ChromaDB, Pinecone, Weaviate, Qdrant, and Milvus, with prescan, batching, validation, and recovery guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[william202404](https://clawhub.ai/user/william202404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to ingest external document collections into a vector database, verify index quality, recover failed ingestion runs, and record ingestion outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ingestion and search scripts are external to the skill and are not pinned or verifiable in the artifact.

Mitigation: Use only scripts from a trusted, pinned source and verify their contents or checksum before running them.

Risk: Knowledge-base ingestion may process sensitive documents and write derived data to a vector database.

Mitigation: Set KB_DIR to the exact intended document set and use least-privileged vector-database credentials.

Risk: Broad source paths can unintentionally index home, project, or shared directories.

Mitigation: Avoid broad directories until path validation is tightened; review the prescan results and confirm the ingestion scope before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/william202404/skills/knowledge-base-ingestion)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment-variable guidance for KB_DIR and VECTOR_DB, batch-size limits, checkpoints, and recovery steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
