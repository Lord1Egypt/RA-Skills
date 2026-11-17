## Description:

This skill helps agents design, build, and troubleshoot production-grade n8n workflows for Qdrant ingestion, retrieval, hybrid search, and RAG pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to plan and implement n8n workflows that ingest source content into Qdrant, enrich metadata, and retrieve context for RAG agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example workflows can expose internal chats, meetings, and documents through ingestion, embeddings, retrieval, or external AI calls.

Mitigation: Restrict approved sources, redact secrets and personal data before external AI calls, and require document-level filters for retrieval.

Risk: Unauthenticated webhooks or destructive Qdrant operations could expose or delete indexed content.

Mitigation: Require authenticated webhooks, human approval for deletions, audit logging, and least-privilege Qdrant credentials.

Risk: Operational defaults may be unsuitable for real company data without additional hardening.

Mitigation: Secure Qdrant and Google Drive backups, define retention and deletion handling, and pin the n8n community node version.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/encryptshawn/skills/n8n-qdrant)
- [n8n Qdrant Node Reference](docs/NODE-REFERENCE.md)
- [Ingestion Pipeline Architecture](docs/INGESTION-PIPELINE.md)
- [RAG Retrieval Patterns in n8n + Qdrant](docs/RAG-RETRIEVAL.md)
- [Chunking Strategy & Metadata Schema Design](docs/CHUNKING-METADATA.md)
- [Collection Setup & Management Workflows](docs/workflows/collection-setup.md)
- [Troubleshooting & Best Practices](docs/TROUBLESHOOTING.md)
- [Qdrant Official n8n Node](https://github.com/qdrant/n8n-nodes-qdrant)
- [Qdrant n8n Platform Docs](https://qdrant.tech/documentation/platforms/n8n)
- [n8n Qdrant Vector Store Docs](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstoreqdrant)
- [Qdrant API Reference](https://api.qdrant.tech/api-reference)
- [FastEmbed](https://github.com/qdrant/fastembed)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with workflow diagrams, JSON examples, JavaScript snippets, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include n8n node settings, Qdrant collection configuration, metadata schemas, workflow JSON, and operational checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
