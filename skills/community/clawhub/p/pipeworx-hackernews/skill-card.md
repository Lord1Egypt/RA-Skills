## Description:

Search and browse Hacker News, including top stories, keyword search through Algolia, and individual item lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search Hacker News discussions, retrieve current top stories, and look up individual stories or comments for digests, research, or linked-item review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connection instructions use an unpinned third-party npm package that can change after review.

Mitigation: Pin mcp-remote to a reviewed exact version and run the bridge in a restricted environment.

Risk: Hacker News queries are sent through Pipeworx, which may expose sensitive search terms to a third-party service.

Mitigation: Avoid confidential company, incident, or research terms unless that data sharing is approved.

## Reference(s):

- [Pipeworx Hacker News pack](https://pipeworx.io/packs/hackernews)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-hackernews)
- [Pipeworx Hacker News MCP endpoint](https://gateway.pipeworx.io/hackernews/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown text with JSON configuration and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for direct examples; MCP connection instructions use npx with mcp-remote.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
