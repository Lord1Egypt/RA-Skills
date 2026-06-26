## Description: <br>
Helps agents design, build, and troubleshoot n8n workflows for Qdrant ingestion, retrieval, hybrid search, and RAG pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to plan production-grade n8n pipelines that ingest source data into Qdrant and retrieve relevant context for RAG workflows. It also helps troubleshoot node selection, chunking, metadata, credentials, indexing, and retrieval quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow examples may move internal messages, documents, prompts, and retrieved context into external AI, vector database, chat, or backup systems. <br>
Mitigation: Restrict source channels and folders, use least-privilege credentials, avoid regulated or secret data unless approved, and add redaction and retention controls before deployment. <br>
Risk: Incorrect delete filters or collection operations can remove more Qdrant data than intended. <br>
Mitigation: Require human approval for destructive operations, validate delete filters against document identifiers, and audit deletions before execution. <br>
Risk: Credentials and backup destinations can expose sensitive source data if configured broadly. <br>
Mitigation: Use scoped Qdrant and source-system credentials, store secrets in n8n credentials or environment variables, and secure any backup destinations used by workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/encryptshawn/n8n-qdrant) <br>
- [Publisher profile](https://clawhub.ai/user/encryptshawn) <br>
- [Qdrant Official n8n Node](https://github.com/qdrant/n8n-nodes-qdrant) <br>
- [Qdrant n8n Platform Docs](https://qdrant.tech/documentation/platforms/n8n) <br>
- [Qdrant n8n Tutorial](https://qdrant.tech/documentation/tutorials-build-essentials/qdrant-n8n/) <br>
- [n8n Qdrant Vector Store Docs](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstoreqdrant) <br>
- [Qdrant API Reference](https://api.qdrant.tech/api-reference) <br>
- [n8n Self-hosted AI Starter Kit](https://github.com/n8n-io/self-hosted-ai-starter-kit) <br>
- [FastEmbed](https://github.com/qdrant/fastembed) <br>
- [Node Reference](docs/NODE-REFERENCE.md) <br>
- [Ingestion Pipeline Architecture](docs/INGESTION-PIPELINE.md) <br>
- [RAG Retrieval Patterns](docs/RAG-RETRIEVAL.md) <br>
- [Chunking Strategy and Metadata Schema Design](docs/CHUNKING-METADATA.md) <br>
- [Troubleshooting and Best Practices](docs/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with workflow diagrams, JSON examples, JavaScript snippets, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; outputs are implementation guidance for n8n and Qdrant workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
