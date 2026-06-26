## Description: <br>
Provides concurrent web search and code search capabilities for agents with hybrid retrieval, including multi-keyword search, URL reading, library search, and library documentation lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebrinass](https://clawhub.ai/user/sebrinass) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to search the web, extract webpage content, and retrieve programming library documentation through SearXNG-backed search and optional embedding re-ranking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation depends on referenced Docker images, npm packages, and an optional Ollama installer. <br>
Mitigation: Install only from trusted sources, prefer pinned versions, and avoid piping remote installer scripts directly into a shell. <br>
Risk: Search queries, prompts, URLs, or extracted content may be exposed to configured search, embedding, or documentation services. <br>
Mitigation: Do not send secrets, confidential prompts, or internal-only URLs through the search and read tools. <br>
Risk: The HTTP service can expose search and read capabilities if bound to an accessible network interface. <br>
Mitigation: Keep the service bound to localhost or protect it with firewall and access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sebrinass/performing-searches) <br>
- [Project homepage](https://github.com/sebrinass/mcp-augmented-search) <br>
- [Installation guide](https://github.com/sebrinass/mcp-augmented-search/blob/main/skill/reference/installation.md) <br>
- [Configuration reference](https://github.com/sebrinass/mcp-augmented-search/blob/main/docs/configuration.md) <br>
- [SearXNG documentation](https://docs.searxng.org) <br>
- [Container image](https://ghcr.io/sebrinass/mcp-augmented-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code] <br>
**Output Format:** [Markdown or JSON-compatible tool responses containing search results, extracted page text, library identifiers, documentation snippets, and code examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search supports up to 3 concurrent keywords; URL reading supports character offsets, maximum length, section extraction, paragraph ranges, and heading-only output.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
