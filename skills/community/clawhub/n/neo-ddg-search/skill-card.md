## Description:

Search the web using DuckDuckGo through a no-API-key Python command-line helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neobotjan2026](https://clawhub.ai/user/neobotjan2026)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run DuckDuckGo searches when current web information is needed and no API-key-backed web search tool is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses --break-system-packages with an unpinned third-party dependency.

Mitigation: Install the dependency in a dedicated virtual environment and pin or review the ddgs package before use.

Risk: Search queries are external network requests and may expose sensitive terms to third-party services.

Mitigation: Keep confidential, personal, and private data out of search queries.

Risk: The skill depends on unofficial DuckDuckGo access through ddgs, so behavior may break or rate-limit under upstream changes or heavy use.

Mitigation: Treat results as availability-dependent, retry or fall back to another search provider when needed, and verify important information from retrieved pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neobotjan2026/skills/neo-ddg-search)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text search results with titles, URLs, and snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the ddgs Python package and external DuckDuckGo availability.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
