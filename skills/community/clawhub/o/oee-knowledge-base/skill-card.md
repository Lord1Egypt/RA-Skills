## Description:

Semantic knowledge base allowing agents to ingest, search, and retrieve saved text, URL, and file content using embeddings and SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odinbot33](https://clawhub.ai/user/odinbot33)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to maintain a local personal knowledge base, ingest notes or web and file content, and retrieve semantically relevant context for follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved content may be sent to remote AI providers for embeddings or answer generation.

Mitigation: Avoid secrets, regulated data, private company documents, and other sensitive content unless remote processing is approved and clearly disclosed.

Risk: URL ingestion can fetch external, internal, or untrusted destinations.

Mitigation: Restrict allowed URL destinations and require confirmation before ingesting private or untrusted links.

Risk: PDF and temporary-file handling require review before use with untrusted documents.

Mitigation: Review and remediate PDF extraction and temporary-file behavior before ingesting untrusted PDFs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odinbot33/skills/oee-knowledge-base)
- [ClawHub publisher profile](https://clawhub.ai/user/odinbot33)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [CLI text output with source citations and optional search-result snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local SQLite knowledge base and may call remote AI providers for embeddings and answers when API keys are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
