## Description:

LLM Wiki helps an agent build and maintain a persistent Obsidian-compatible markdown knowledge base by ingesting sources, compiling cross-linked wiki pages, answering grounded queries, linting the graph, and processing audit feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juliahzhu](https://clawhub.ai/user/juliahzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge-base maintainers use this skill to turn raw articles, papers, notes, and feedback into a structured local markdown wiki. It supports long-running research deep-dives, personal or team knowledge bases, reading companions, graph linting, and durable audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently creates and modifies files under the chosen wiki root.

Mitigation: Review proposed changes before broad ingest, audit, or cleanup runs.

Risk: Wiki content may accidentally include secrets or sensitive material from local sources.

Mitigation: Avoid storing secrets in the wiki and review raw sources before ingest.

Risk: Optional npm and pip tooling can introduce dependency exposure.

Mitigation: Pin and isolate optional npm and pip tooling before use.

Risk: Generated HTML and JavaScript outputs can behave as active content.

Mitigation: Treat generated HTML and JavaScript outputs as untrusted until reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juliahzhu/skills/llm-wiki-q)
- [Karpathy llm-wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Obsidian](https://obsidian.md)
- [qmd](https://github.com/tobi/qmd)
- [CLAUDE.md Schema Guide](references/schema-guide.md)
- [Wiki Article Writing Guide](references/article-guide.md)
- [Audit Guide](references/audit-guide.md)
- [Log Guide](references/log-guide.md)
- [Tooling Tips](references/tooling-tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, wiki directory structures, lint and audit reports, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent local files under the selected wiki root, including raw source notes, wiki pages, query outputs, audit records, and daily operation logs.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
