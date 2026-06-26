## Description: <br>
Design and build hybrid retrieval systems that combine BM25 keyword search, vector embeddings, and knowledge graph traversal for agent memory and RAG workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vnesin-sarai](https://clawhub.ai/user/vnesin-sarai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose retrieval layers, storage backends, embedding models, chunking strategies, fusion weights, and evaluation approaches for hybrid RAG or agent memory systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A retrieval system may index documents the agent is not approved to use. <br>
Mitigation: Define approved document sources before ingestion and apply access controls to indexed content. <br>
Risk: Sensitive text may be sent to a cloud embedding provider. <br>
Mitigation: Use an approved embedding provider or self-hosted model, and redact sensitive content when required. <br>
Risk: API keys or database credentials may be exposed while configuring retrieval services. <br>
Mitigation: Manage secrets outside shared chat context and store credentials in approved secret-management systems. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/vnesin-sarai/hybrid-retrieval) <br>
- [BlackRock/NVIDIA HybridRAG Paper](https://arxiv.org/abs/2408.04948) <br>
- [Qdrant](https://qdrant.tech/) <br>
- [sqlite-vec](https://github.com/asg017/sqlite-vec) <br>
- [Neo4j](https://neo4j.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with SQL, Python, and Cypher examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no executable installer was found in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
