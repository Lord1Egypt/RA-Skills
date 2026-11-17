## Description:

Builds and manages a local RAG workflow with environment setup, embedding model downloads, document splitting, vector knowledge bases, prompt templates, and optional Web UI configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up local retrieval-augmented generation, import documents into local vector knowledge bases, retrieve context for an agent, or run a standalone local-LLM RAG loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Web UI is unauthenticated and should not be exposed on a shared network.

Mitigation: Bind the Web UI to loopback, add authentication before broader exposure, and avoid running it where untrusted clients can reach it.

Risk: Model download paths and custom model identifiers can pull code or model artifacts from external sources.

Mitigation: Use trusted model identifiers only, pin dependencies and model sources, and review downloaded artifacts before deployment.

Risk: Standalone RAG mode can send retrieved context to a configured LLM endpoint.

Mitigation: Use only trusted local or remote LLM endpoints and treat indexed documents and retrieved context as sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/local-rag-builder)
- [Architecture](references/architecture.md)
- [Usage guide](references/guide.md)
- [External LLM setup](references/llm-setup.md)
- [Permissions and test report](references/permissions.md)
- [Examples](references/examples.md)
- [FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and command examples, with JSON available from CLI retrieval and management commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return retrieved context, source document metadata, filled prompts, knowledge-base status, environment reports, and configuration updates.]

## Skill Version(s):

1.6.0 (source: server release metadata; artifact frontmatter reports 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
