## Description:

Extract web data, capture screenshots, scrape content, and generate AI images via OpenGraph.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[primeobsession](https://clawhub.ai/user/primeobsession)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and AI agents use this skill to turn URLs into metadata, screenshots, rendered HTML, page answers, and generated visual assets through OpenGraph.io APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs, page content, screenshots, prompts, and generated asset data are sent to OpenGraph.io.

Mitigation: Use the skill only for pages and prompts approved for external processing; avoid private, authenticated, regulated, or internal content unless approval is documented.

Risk: The optional MCP setup can execute an npm package locally.

Mitigation: Prefer a pinned and reviewed MCP package version, or use the REST API examples directly when local package execution is not required.

Risk: Proxy-based scraping can access pages in ways that may conflict with authorization, site terms, or law.

Mitigation: Use proxy options only for authorized access that complies with applicable site terms, policies, and legal requirements.

Risk: The OpenGraph App ID is a credential-like secret.

Mitigation: Store the App ID in approved secret handling paths such as environment variables or protected client configuration, and avoid exposing it in logs, prompts, or shared files.

## Reference(s):

- [OpenGraph.io Skill Page](https://clawhub.ai/primeobsession/skills/opengraph-io-skill)
- [OpenGraph.io Website](https://www.opengraph.io)
- [OpenGraph.io Documentation](https://www.opengraph.io/documentation)
- [API Reference](references/api-reference.md)
- [For AI Agents](references/for-ai-agents.md)
- [Image Generation Reference](references/image-generation.md)
- [MCP Client Setup](references/mcp-clients.md)
- [Platform Support](references/platform-support.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Examples](examples/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON request examples, configuration snippets, and generated asset links or files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include OpenGraph metadata, screenshots, scraped HTML, page-query answers, image-generation session details, asset IDs, and downloadable image files.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
