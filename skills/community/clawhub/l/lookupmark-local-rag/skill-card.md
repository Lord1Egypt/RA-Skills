## Description:

Semantic search over local files using all-MiniLM-L6-v2 embeddings, ms-marco-MiniLM-L-6-v2 reranking, ChromaDB, and parent-child chunking for document retrieval on low-RAM ARM devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lookupmark](https://clawhub.ai/user/lookupmark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to index local document folders and answer natural-language questions from retrieved file context without sending files to a web search service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and persist chunks from local document folders, including unintended sensitive files.

Mitigation: Index only trusted, intended folders; review the configured allowed roots and blocked patterns before running indexing.

Risk: The skill persists private search data in a local ChromaDB store and query log.

Mitigation: Treat the local data directory as sensitive, restrict account access, and clear the index or query log when the data is no longer needed.

Risk: Batch indexing can disrupt local indexing processes when run unattended or from privileged accounts.

Mitigation: Avoid privileged execution, monitor batch runs, and do not index shared or untrusted folders until path containment, symlink handling, query-log controls, and cleanup behavior are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lookupmark/skills/lookupmark-local-rag)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; query output can be plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include file paths, relevance scores, matched snippets, and parent context; query text is truncated in the local query log.]

## Skill Version(s):

1.9.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
