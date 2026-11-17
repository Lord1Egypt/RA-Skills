## Description:

Multi-Web-Search is a no-API-key web search skill that runs multi-engine text, image, news, video, and book searches with time, site, proxy, cache, and fallback support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzairong](https://clawhub.ai/user/wangzairong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent search current web, technical, news, image, video, and book sources without configuring an API key. It is suited for multi-language search, site-restricted search, and search workflows that can tolerate third-party search-engine exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to third-party search engines.

Mitigation: Use the skill only for queries that can be shared with external search providers.

Risk: Proxy credentials or sensitive query details may appear in output or local cache.

Mitigation: Avoid credentials in proxy URLs and use --no-cache for sensitive searches.

Risk: The installer can install an unpinned third-party package into the user environment.

Mitigation: Install ddgs separately in an isolated environment with pinned versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzairong/skills/multi-web-search)
- [Release changelog](artifact/CHANGELOG.md)
- [Artifact metadata](artifact/metadata.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON search-result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results can include titles, URLs, snippets, source engines, result counts, cache flags, DHT status, and proxy status.]

## Skill Version(s):

3.4.0 (source: frontmatter, changelog, metadata, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
