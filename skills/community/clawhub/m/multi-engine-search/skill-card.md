## Description:

Unified multi-engine web search for finding information, looking up sources, and performing research across Tavily, Google, Bing, Baidu, and DuckDuckGo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run quick lookups and broader research across API-based and browser-based search engines, including Chinese-language and aggregated searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to external providers, including Tavily and browser-based search engines.

Mitigation: Avoid sending sensitive or confidential queries unless the selected provider is approved for that data.

Risk: The skill may execute a neighboring Tavily helper package when that package is present.

Mitigation: Review or remove the automatic sibling-package Tavily execution path before using the skill in sensitive environments.

## Reference(s):

- [Search Engine Reference](references/engines.md)
- [Tavily](https://tavily.com)
- [ClawHub Skill Page](https://clawhub.ai/shenmeng/skills/multi-engine-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [JSON search results or Markdown result lists with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include titles, URLs, snippets, provider errors, source engine names, and Tavily answer summaries when requested.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
