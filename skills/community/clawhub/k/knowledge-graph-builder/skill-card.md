## Description:

Builds an interactive force-directed HTML knowledge graph from a structured knowledge vault by scanning INDEX.md, article metadata, framework nodes, and configurable links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milesnee](https://clawhub.ai/user/milesnee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base maintainers use this skill to build, update, verify, and optionally serve an interactive graph from structured vault content. It is suited for visualizing cross-domain relationships using indexed articles, frame_analysis metadata, framework nodes, category mappings, keyword co-occurrence, and manual links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML or optional serving can expose private vault content.

Mitigation: Review the graph before sharing, serve only a dedicated publish directory, prefer localhost for private vaults, and avoid the 0.0.0.0 server example for private content.

Risk: Untrusted Markdown, configuration, or title content can lead to injected browser code in the generated HTML.

Mitigation: Use trusted vault inputs, validate or escape custom content before generation, and inspect generated HTML before opening or publishing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/milesnee/skills/knowledge-graph-builder)
- [INDEX.md classification reference](references/index-classification.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide generation of a self-contained Canvas HTML graph file when the bundled Python script is run.]

## Skill Version(s):

1.2.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
