## Description:

Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to choose and compose searches across domestic and international search engines, including advanced operators, time filters, privacy-oriented engines, and WolframAlpha knowledge queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to external search providers and may expose sensitive or confidential information.

Mitigation: Avoid secrets, credentials, personal data, and confidential investigation terms; use privacy-oriented engines and safe-search or family-filter settings when appropriate.

Risk: Some documentation is Chinese-only and a referenced domestic search guide is not included in the package.

Mitigation: Verify search syntax against the packaged international guide or provider documentation before relying on unsupported domestic examples.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bingze00000/skills/multi-search-engine-jarvis)
- [International Search Guide](artifact/references/international-search.md)
- [DuckDuckGo Bangs](https://duckduckgo.com/bang)
- [WolframAlpha Examples](https://www.wolframalpha.com/examples/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown with search URLs and web_fetch examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys required; search terms are sent to selected external search providers.]

## Skill Version(s):

2.0.2 (source: release evidence and artifact/_meta.json; packaged docs mention v2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
