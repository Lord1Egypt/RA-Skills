## Description:

Provides local and optional hybrid retrieval over the Mao Selected Works 1-7 corpus, returning source-grounded passages by volume, article, title, or keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henryczq](https://clawhub.ai/user/henryczq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search the Mao Selected Works corpus, locate articles and passages, and return verifiable source paths and retrieval modes. It supports default local keyword search and optional remote embedding/reranking when explicitly configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional RAG can send queries and corpus passages to a configured remote embedding or reranking endpoint.

Mitigation: Keep local search as the default, and enable RAG only with a trusted HTTPS provider and a dedicated low-privilege API key.

Risk: Retrieved historical political text may include violent, repressive, weapons-related, or protected-group content.

Mitigation: Present passages as historical source material with clear citations and avoid treating retrieved text as policy, endorsement, or operational advice.

Risk: Search results can be incomplete when title, alias, metadata, or index coverage is insufficient.

Mitigation: Report no-match conditions plainly, include retrieval mode and source path, and suggest alternate terms or metadata cleanup instead of inventing answers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/henryczq/skills/mao-selected-works)
- [Corpus Format](artifact/references/corpus-format.md)
- [Retrieval Rules](artifact/references/retrieval-rules.md)
- [Output Schema](artifact/references/output-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and optional JSON search results with source metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results should include volume, article title, source path, retrieval mode, and snippet when available.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
