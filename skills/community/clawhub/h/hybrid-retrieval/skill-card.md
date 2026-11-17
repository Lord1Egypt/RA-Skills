## Description:

Design and build a hybrid retrieval system combining BM25 keyword search, vector embeddings, and knowledge graph traversal for AI agent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnesin-sarai](https://clawhub.ai/user/vnesin-sarai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design agent memory and RAG retrieval systems that combine BM25, vector search, and graph traversal for better recall quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real documents, chats, emails, or agent memory may be sent to external embedding providers or stored in long-lived search indexes.

Mitigation: Review data classification, retention, and provider policies before applying the recommendations to production data.

Risk: Retrieval design advice may produce incomplete or misleading results if adopted without evaluation on representative queries.

Mitigation: Create test queries with expected results and tune chunking, fusion weights, thresholds, and reranking against that evaluation set.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vnesin-sarai/skills/hybrid-retrieval)
- [BlackRock/NVIDIA HybridRAG Paper](https://arxiv.org/abs/2408.04948)
- [Qdrant](https://qdrant.tech/)
- [sqlite-vec](https://github.com/asg017/sqlite-vec)
- [Neo4j](https://neo4j.com/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with SQL, Python, and Cypher code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend retrieval architecture choices, storage backends, embedding models, chunking strategy, fusion weights, and evaluation setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
