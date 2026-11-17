## Description:

Provides concurrent web search, URL reading, and programming documentation search for agents using SearXNG with optional embedding re-ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebrinass](https://clawhub.ai/user/sebrinass)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to add local web search, page reading, and programming library documentation retrieval to an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and deployment examples use mutable third-party package and container references.

Mitigation: Pin npm package versions and container image digests before deployment.

Risk: The local HTTP service and SearXNG ports may be exposed more broadly than intended.

Mitigation: Bind ports to 127.0.0.1 or a private network and add authentication before remote access.

Risk: Search queries, fetched URLs, and optional embedding content may be sent to configured upstream providers.

Mitigation: Use trusted SearXNG and embedding providers, and avoid public search instances for sensitive queries.

Risk: Shell installation snippets can execute remote installer scripts.

Mitigation: Review installer scripts before execution and avoid curl-piped shell execution in controlled environments.

## Reference(s):

- [Installation Guide](reference/installation.md)
- [ClawHub Skill Page](https://clawhub.ai/sebrinass/skills/performing-searches)
- [Augmented Search Repository](https://github.com/sebrinass/mcp-augmented-search)
- [Configuration Reference](https://github.com/sebrinass/mcp-augmented-search/blob/main/docs/configuration.md)
- [SearXNG Documentation](https://docs.searxng.org)
- [Docker Image](https://ghcr.io/sebrinass/mcp-augmented-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return search results, extracted webpage content, library identifiers, and documentation excerpts depending on the invoked tool.]

## Skill Version(s):

1.1.3 (source: server release metadata; artifact frontmatter lists 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
