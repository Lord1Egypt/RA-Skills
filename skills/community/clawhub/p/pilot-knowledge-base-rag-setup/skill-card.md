## Description: <br>
Deploy a four-agent knowledge base RAG pipeline for document ingestion, embedding, vector indexing, and query serving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to set up a multi-host retrieval-augmented generation pipeline that ingests documents, creates embeddings, stores vectors, and serves search queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup exchanges document chunks, embeddings, search queries, and ranked results across multiple hosts. <br>
Mitigation: Restrict network access to trusted hosts and verify peer identities before completing handshakes. <br>
Risk: Ingested documents may contain sensitive or regulated data. <br>
Mitigation: Use the skill only where permissions, encryption, access control, audit logging, and retention rules are already defined. <br>
Risk: The pipeline depends on multiple Pilot skills and local binaries. <br>
Mitigation: Review dependent skills and confirm `pilotctl`, `clawhub`, and the Pilot daemon are installed before deployment. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands and JSON manifest snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces per-role setup instructions for ingest, embedder, indexer, and query agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
