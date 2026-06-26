## Description: <br>
Unified multi-engine web search for web lookup and research across Tavily, Google, Bing, Baidu, and DuckDuckGo, with optional result aggregation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run quick lookups or broader research queries through Tavily or browser-based search engines. It is especially useful when comparing coverage across providers or searching Chinese-language content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may be sent to Tavily or browser-based providers outside the user's environment. <br>
Mitigation: Avoid searching secrets or sensitive personal or business data, choose the search provider deliberately, and use a scoped Tavily API key. <br>
Risk: The skill can run a sibling Tavily helper outside the reviewed package when that helper is present. <br>
Mitigation: Review the sibling Tavily helper before installing or using the skill, and deploy only reviewed helper code in trusted environments. <br>
Risk: Browser-based search depends on the installed agent-browser tool and live search pages. <br>
Mitigation: Enable browser-based engines only when the installed browser tool is trusted and users are comfortable sending queries to the selected provider. <br>


## Reference(s): <br>
- [Search Engine Reference](references/engines.md) <br>
- [ClawHub Release Page](https://clawhub.ai/shenmeng/multi-engine-search) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON or Markdown search results, with an optional Tavily answer summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default result limit is 5; aggregated search combines Tavily, Google, and Baidu results and deduplicates by URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
