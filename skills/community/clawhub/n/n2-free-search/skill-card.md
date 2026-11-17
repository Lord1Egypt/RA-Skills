## Description:

Free, unlimited web search for AI agents via SearXNG; no API keys are needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choihyunsus](https://clawhub.ai/user/choihyunsus)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to add MCP-based web, news, image, video, and suggestion search to AI agents using public or self-hosted SearXNG.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned npm package locally can execute changed package code in the MCP client environment.

Mitigation: Pin or otherwise verify the npm package version before adding it to an MCP client configuration.

Risk: Public search mode may expose search queries to an external search service.

Mitigation: Use self-hosted SearXNG mode for sensitive work and avoid sending secrets or private data in public search queries.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/choihyunsus/skills/n2-free-search)
- [Publisher profile](https://clawhub.ai/user/choihyunsus)
- [NPM package](https://www.npmjs.com/package/n2-free-search)
- [Project website](https://nton2.com)
- [Repository listed in artifact metadata](https://github.com/choihyunsus/n2-free-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON MCP configuration examples and text search results from MCP tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP tools cover web, news, image, video, and suggestion searches; public mode sends queries to an external search service, while self-hosted mode can use a local SearXNG endpoint.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
