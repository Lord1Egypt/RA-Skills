## Description:

Query local Google OKF v0.2 and Obsidian Markdown meeting-notes vaults offline via stdio MCP or CLI (search transcripts by speaker/date, extract open - [ ] action items, resolve [[wiki-links]] and incoming backlinks).

This skill is ready for commercial/non-commercial use.

## Publisher:

[rootpjh](https://clawhub.ai/user/rootpjh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use the skill to search local meeting transcripts and Obsidian notes, review open action items, and follow wiki links through MCP or the CLI while keeping the vault local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI example invokes unpinned GitHub code, which could change after review.

Mitigation: Review the upstream project and use a reviewed, fixed version; limit access to the vault files and network the tool needs.

## Reference(s):

- [MCP Integration Docs](https://onemira.com/docs/mcp-integration)
- [Obsidian & Local Markdown Workflow Guide](https://onemira.com/blogs/ai-voice-recorder-for-obsidian-and-local-markdown)
- [OneMira C1 Product Information](https://onemira.com/products/c1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown responses with search results, vault statistics, action items, and wiki-link context; inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
