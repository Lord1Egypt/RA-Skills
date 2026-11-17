## Description:

Local retrieval skill for large documentation corpora using independent SQLite knowledge libraries with keyword plus vector hybrid search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mozi1924](https://clawhub.ai/user/mozi1924)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use LiteRAG to index, search, inspect, benchmark, and tune retrieval over large external documentation corpora without placing those corpora in main agent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace configuration can cause LiteRAG to read broad local paths, including content that should not be indexed.

Mitigation: Review .literag/knowledge-libs.json before indexing, restrict source paths to intended documentation, and use excludes for sensitive or irrelevant files.

Risk: A configured remote OpenAI-compatible embedding endpoint may receive document text, queries, and bearer tokens.

Mitigation: Use a trusted local embedding endpoint by default, or explicitly approve the remote endpoint and credentials before indexing or searching.

Risk: The sqlite-vec dependency affects vector search behavior and production risk.

Mitigation: Pin or review sqlite-vec before production use and verify the selected Python and SQLite runtime support the expected vector backend.

## Reference(s):

- [LiteRAG ClawHub Release](https://clawhub.ai/mozi1924/skills/literag)
- [LiteRAG Homepage](https://github.com/little-jax/literag)
- [Usage Guide](references/usage.md)
- [Configuration Reference](references/configuration.md)
- [Agent Prompt Templates](references/agent-prompts.md)
- [Optimization Playbook](references/optimization-playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and inspect commands can emit literag.search.v2 and literag.inspect.v1 payloads; indexes and metadata are stored in workspace-local SQLite libraries.]

## Skill Version(s):

0.2.2 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
