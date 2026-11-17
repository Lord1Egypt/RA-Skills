## Description:

Cross-project knowledge graph powered by local FalkorDB that indexes project recaps, plans, memory files, architecture docs, and skills across configured projects for concept-based querying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adelvillar1](https://clawhub.ai/user/adelvillar1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build and query a local, persistent index of project knowledge across multiple repositories and skill directories, especially when retrieving prior decisions, recaps, plans, and implementation patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent indexing of broad project documents can retain sensitive or stale content beyond the source file lifecycle.

Mitigation: Run the dry run before indexing, narrow PROJECT_ROOTS to intentional locations, and purge or delete indexed chunks when content should no longer be searchable.

Risk: Setting KNOWLEDGE_FALKORDB_HOST away from localhost can send document contents to a remote FalkorDB server.

Mitigation: Keep KNOWLEDGE_FALKORDB_HOST unset or pointed at localhost unless remote transfer is intentional and approved.

Risk: Using falkordb/falkordb:latest relies on a mutable container image.

Mitigation: Use a digest-pinned FalkorDB image for controlled deployments.

## Reference(s):

- [Backend Storage Evaluation: SQLite vs FalkorDB](references/falkordb-vs-sqlite-evaluation.md)
- [Project Knowledge Graph on ClawHub](https://clawhub.ai/adelvillar1/skills/project-knowledge-graph)
- [Publisher Homepage](https://github.com/adelvillar1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and Python CLI usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker, a local FalkorDB service, and falkordb==1.6.1; writes indexed chunks to a persistent Docker volume.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
