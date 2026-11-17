## Description:

Semantic search over workspace markdown files using an OpenAI-compatible embedding API and SQLite vector store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toller892](https://clawhub.ai/user/toller892)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to index workspace Markdown files and retrieve semantically related notes, decisions, and context by meaning rather than exact keyword match. It is not intended for non-Markdown, web, or code search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace Markdown content and search queries may be sent to the configured embedding provider.

Mitigation: Use only trusted HTTPS or local embedding endpoints, scope indexing to the minimum necessary workspace paths, and exclude secrets, regulated data, and private notes that should not leave the environment.

Risk: The SQLite database stores plaintext Markdown snippets alongside embeddings.

Mitigation: Treat the database as sensitive, store it in a controlled path with appropriate access permissions, and remove it when the index is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/toller892/skills/memory-semantic-search)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text search results or JSON array of result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include file paths, line ranges, cosine similarity scores, and content snippets; indexing creates a local SQLite database of Markdown chunks and embeddings.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
