## Description:

Deploys a four-agent RAG pipeline for document ingestion, embedding, vector indexing, and query serving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up a knowledge base RAG deployment across ingest, embedding, indexing, and query agents. It provides role-specific setup guidance, dependency installation commands, handshakes, manifests, and example data-flow commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs multiple integration skills without pinned versions.

Mitigation: Pin and verify every dependent skill before deployment.

Risk: The pipeline auto-establishes trust between agents that handle documents, embeddings, queries, and results.

Mitigation: Validate the deployment prefix, confirm peer identities before handshakes, and restrict each role's credentials to only what it needs.

Risk: Deployments may process private documents, production S3 buckets, vector databases, or public query endpoints.

Mitigation: Set retention, audit, and access controls for documents, embeddings, queries, and results.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-knowledge-base-rag-setup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes role-specific hostnames, skill installation commands, handshake steps, manifest templates, and workflow examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
