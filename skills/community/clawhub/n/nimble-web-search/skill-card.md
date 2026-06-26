## Description: <br>
Real-time web intelligence powered by Nimble Search API for current web search, URL discovery, focused research, and source-backed summaries across specialized focus modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilchemla](https://clawhub.ai/user/ilchemla) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and agent users use this skill to retrieve current web results, discover relevant URLs, monitor news or products, and synthesize findings from Nimble Search API responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the Nimble API key are sent to Nimble's external search API. <br>
Mitigation: Use a dedicated revocable Nimble API key and avoid including secrets or confidential project details in search queries. <br>
Risk: Search results, summaries, URLs, or extracted page content may contain sensitive information if stored locally. <br>
Mitigation: Limit local caching and handle saved search outputs according to the sensitivity of the source material. <br>


## Reference(s): <br>
- [Nimble Search API Reference](references/api-reference.md) <br>
- [Focus Modes - Complete Guide](references/focus-modes.md) <br>
- [Search Strategies - Best Practices](references/search-strategies.md) <br>
- [Nimble](https://www.nimbleway.com/) <br>
- [Nimble Search API endpoint](https://nimble-retriever.webit.live/search) <br>
- [Repository metadata](https://github.com/Nimbleway/agent-skills) <br>
- [ClawHub release page](https://clawhub.ai/ilchemla/nimble-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples, shell commands, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include source URLs, titles, descriptions, generated answers, and extracted page content when deep search is enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
