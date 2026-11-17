## Description:

Multi search engine integration for 17 Chinese and global engines that supports advanced operators, time filters, site search, privacy-focused engines, and WolframAlpha knowledge queries without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reknottycat](https://clawhub.ai/user/reknottycat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to construct search queries across Chinese and global search engines, compare results, apply advanced operators, and route knowledge queries to WolframAlpha.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to external providers, which can expose sensitive terms, personal data, secrets, or internal URLs.

Mitigation: Do not use confidential queries with this skill; review generated URLs before fetching and prefer privacy-focused engines only when their terms are acceptable.

Risk: Artifact examples include unsafe patterns for locating login/admin pages and exposed password text.

Mitigation: Remove or ignore password, admin-page, and exposed-secret discovery examples before use or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reknottycat/skills/multi-search-engine-local)
- [International search guide](references/international-search.md)
- [Changelog](CHANGELOG.md)
- [DuckDuckGo Bangs](https://duckduckgo.com/bang)
- [WolframAlpha examples](https://www.wolframalpha.com/examples/)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with URL examples and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys required; generated search URLs send query text to external search providers.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact files list v2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
