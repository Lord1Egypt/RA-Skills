## Description:

This skill provides semantic search over your memory files using a local vector database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[royhk920](https://clawhub.ai/user/royhk920)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to index local memory Markdown files and retrieve relevant memories through semantic or hybrid search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can index private memory and additional workspace Markdown directories.

Mitigation: Review configured source directories before installation and set MEMORY_PRO_EXTRA_MD_DIRS to an empty value unless extra workspace Markdown should be indexed.

Risk: Optional reranking can send search queries and retrieved memory snippets to a configured external provider.

Mitigation: Keep MEMORY_PRO_ENABLE_RERANK disabled unless external reranking is intended, and use only trusted rerank endpoints.

Risk: BM25 pickle artifacts and benchmark outputs can contain sensitive local-memory data.

Mitigation: Treat BM25 artifacts and /tmp benchmark outputs as sensitive local files and avoid sharing them.

## Reference(s):

- [Memory Pro ClawHub page](https://clawhub.ai/royhk920/skills/memory-pro)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text or JSON search results, with shell commands and configuration guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search responses include ranked memory snippets and scores; hybrid mode can include debug scoring metadata.]

## Skill Version(s):

2.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
