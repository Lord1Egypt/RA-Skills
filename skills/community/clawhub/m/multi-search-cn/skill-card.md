## Description:

Aggregates Chinese-language web search by fetching DuckDuckGo HTML results with the cn-zh locale and generating direct links to Bing China, Baidu, Sogou, and 360 search pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottliu007](https://clawhub.ai/user/scottliu007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and external users can use this skill to retrieve Chinese-locale search results and fallback direct search links when domestic search coverage or Chinese-language web discovery is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms may be sent to DuckDuckGo during parsed-result mode and may be embedded in links for Chinese search providers.

Mitigation: Avoid sensitive or private queries unless that disclosure is acceptable; use urls-only mode when only generated links are needed.

Risk: Parsed web results may fail or be incomplete because search providers can rate limit, change page structure, or require browser-side checks.

Mitigation: Disclose fetch failures or empty results and provide direct search links so users can verify results in a browser.

Risk: High-frequency automated queries may violate provider terms or trigger abuse protections.

Mitigation: Keep query frequency low and follow the search providers' robots and service terms.

## Reference(s):

- [Multi-Search-CN Reference](reference.md)
- [ClawHub Skill Page](https://clawhub.ai/scottliu007/skills/multi-search-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown search results or JSON, with direct search URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [DuckDuckGo parsed results default to a limit of 8; urls-only mode emits search links without fetching result pages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
