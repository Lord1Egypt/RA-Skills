## Description:

Graph-native memory engine for AI agents with hybrid vector and keyword search, biological decay, Zettelkasten linking, trust-gated conflict resolution, explainability, episodes, compression, and consolidation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremiaheth](https://clawhub.ai/user/jeremiaheth)

### License/Terms of Use:

Elastic-2.0

## Use Case:

Developers and agent builders use this skill to add persistent, searchable, graph-linked memory to AI agents, including recall across sessions, conflict-aware updates, and optional semantic search or LLM-assisted maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI examples can create package-resolution risk if copied as unscoped npx commands.

Mitigation: Install and run the scoped package with pinned or local commands, such as npm install --save-exact @jeremiaheth/neolata-mem@0.8.4 followed by the local binary.

Risk: Stored memories, embeddings, markdown write-through files, webhook payloads, and Supabase rows can contain sensitive agent or user context.

Mitigation: Start with in-memory or local JSON storage for evaluation, restrict file and database access, use Supabase anon keys with RLS, and configure only trusted webhook endpoints.

Risk: All-agent recall can expose memories across agent boundaries when cross-agent sharing is not intended.

Mitigation: Scope recall to the intended agent or session, and use cross-agent context only when the deployment explicitly requires shared memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeremiaheth/skills/neolata-mem)
- [Project homepage](https://github.com/Jeremiaheth/neolata-mem)
- [npm package](https://www.npmjs.com/package/@jeremiaheth/neolata-mem)
- [User Guide](references/guide.md)
- [Practical Implementation Notes](references/implementation-notes.md)
- [Runtime Helpers](references/runtime-helpers.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript examples, shell command snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local JSON storage, in-memory evaluation, optional embedding or LLM providers, Supabase storage, webhook write-through, and multi-agent recall behavior.]

## Skill Version(s):

0.8.5 (source: server release metadata; artifact frontmatter reports 0.8.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
