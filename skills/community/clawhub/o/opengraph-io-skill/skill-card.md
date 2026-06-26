## Description: <br>
Extract web data, capture screenshots, scrape content, and generate AI images via OpenGraph.io. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[primeobsession](https://clawhub.ai/user/primeobsession) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI assistant users use this skill to fetch URL metadata, screenshots, rendered HTML, selected elements, AI page answers, and generated images through OpenGraph.io APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send URLs, page content, screenshots, prompts, and generated-image requests to a third-party service. <br>
Mitigation: Use only public or clearly authorized URLs and do not send secrets, private/internal links, session-bound pages, personal data, or confidential prompts. <br>
Risk: Scraping and proxy options could be used to bypass site controls, rate limits, paywalls, geo-restrictions, or bot protections. <br>
Mitigation: Keep proxy and auto-proxy features disabled unless the user has authorization and the target site's terms allow the access pattern. <br>
Risk: The optional MCP setup installs and runs an npm package. <br>
Mitigation: Verify the package source before use and pin a trusted version for managed environments. <br>


## Reference(s): <br>
- [OpenGraph.io](https://www.opengraph.io) <br>
- [OpenGraph.io API Documentation](https://www.opengraph.io/documentation) <br>
- [OpenGraph.io Dashboard](https://dashboard.opengraph.io) <br>
- [API Reference](references/api-reference.md) <br>
- [AI Agent Reference](references/for-ai-agents.md) <br>
- [Image Generation Reference](references/image-generation.md) <br>
- [MCP Client Setup](references/mcp-clients.md) <br>
- [Platform Support Guide](references/platform-support.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [OpenGraph.io MCP Server](https://github.com/securecoders/opengraph-io-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include third-party API responses, URLs to generated or captured assets, and setup guidance requiring OPENGRAPH_APP_ID.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
