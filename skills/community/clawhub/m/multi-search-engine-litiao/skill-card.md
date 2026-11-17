## Description:

Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to construct search URLs and search guidance across Chinese and global search engines for web research, site-specific search, time-filtered queries, privacy-oriented search, and WolframAlpha knowledge queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to the selected external search provider and may expose secrets, credentials, private URLs, personal data, or confidential project names.

Mitigation: Use safe-search defaults unless deliberately changing them, and avoid submitting secrets, credentials, private URLs, personal data, or confidential project names as search queries.

## Reference(s):

- [International Search Guide](references/international-search.md)
- [ClawHub Skill Page](https://clawhub.ai/litiao1224/skills/multi-search-engine-litiao)
- [DuckDuckGo Bangs](https://duckduckgo.com/bang)
- [WolframAlpha Examples](https://www.wolframalpha.com/examples/)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with search URL templates and web_fetch examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys required; queries are sent to selected external search providers.]

## Skill Version(s):

1.0.0 (source: server release metadata); artifact documentation reports 2.0.1

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
