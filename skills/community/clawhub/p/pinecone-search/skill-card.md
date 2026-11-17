## Description:

Pinecone vector search and document upload tool for knowledge base management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deki18](https://clawhub.ai/user/deki18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to upload local TXT and Markdown documents into a Pinecone vector index, then search that knowledge base with semantic and keyword-assisted retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded document text and local file paths can be sent to external Pinecone and embedding services and may persist in Pinecone.

Mitigation: Use only approved Pinecone and embedding accounts, avoid broad or private directories unless authorized, and review uploaded content before indexing.

Risk: Dry-run mode may still initialize remote services or create a Pinecone index.

Mitigation: Do not rely on dry-run as non-mutating; use an isolated account or test index until the behavior is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deki18/skills/pinecone-search)
- [Repository homepage](https://github.com/deki18/pinecone-search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Command-line text output and optional JSON upload statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output includes matched document metadata and snippets; upload output can include file, chunk, success, failure, token, namespace, and duration statistics.]

## Skill Version(s):

0.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
