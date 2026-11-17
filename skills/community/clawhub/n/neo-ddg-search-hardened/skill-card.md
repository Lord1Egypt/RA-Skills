## Description:

Search the web using DuckDuckGo without an API key and return results with titles, URLs, and snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve current web search results through DuckDuckGo, especially when a built-in web search tool is unavailable or not configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses an overbroad system Python package installation method.

Mitigation: Install ddgs in a virtual environment with pinned versions and hashes instead of using --break-system-packages.

Risk: Search result titles, snippets, and URLs can contain prompt injection or social engineering content.

Mitigation: Treat all search results as untrusted external data and do not execute commands or follow instructions embedded in results.

Risk: Fetching private-network or internal URLs from search results can expose server-side request forgery risk.

Mitigation: Only fetch publicly routable URLs and refuse localhost, private IP ranges, link-local addresses, and internal service endpoints.

Risk: Search queries or results may contain sensitive data that should not be forwarded to external services.

Mitigation: Keep search output local and do not pipe, redirect, email, or send it to webhooks, APIs, or remote servers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/neo-ddg-search-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/neo-ddg-search)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands]

**Output Format:** [Plain text result list with a title, URL, and snippet for each result.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result count defaults to 5 and can be set up to 20; availability depends on ddgs and DuckDuckGo.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
