## Description:

Validate Open Knowledge Format (OKF v0.2) Markdown vaults, convert WebVTT (.vtt) and SubRip (.srt) speaker-labeled meeting transcripts into deterministic OKF session notes, and build [[wiki-link]] relational knowledge graphs for Obsidian, Claude MCP, Cursor, and OneMira local context workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rootpjh](https://clawhub.ai/user/rootpjh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use the skill to convert meeting transcripts into OKF notes, validate vault frontmatter and links, and export a relational knowledge graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an unpinned GitHub package in its commands, so the executed code could change after review; scanner coverage was partial and did not inspect every referenced path.

Mitigation: Review the package and use a reviewed fixed version before running its commands.

## Reference(s):

- [OKF Local Wiki Specification](https://onemira.com/docs/daily-use/local-wiki)
- [MCP & CLI Agent Workflow](https://onemira.com/docs/mcp-integration)
- [OneMira C1](https://onemira.com/products/c1)
- [OKF Markdown on ClawHub](https://clawhub.ai/rootpjh/skills/okf-markdown)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands]

**Output Format:** [OKF Markdown notes, JSON graph exports, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works with supplied transcript files and Markdown vaults.]

## Skill Version(s):

1.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
