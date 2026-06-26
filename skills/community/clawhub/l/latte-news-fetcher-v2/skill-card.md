## Description: <br>
Fetches current news and RSS-oriented digests from free public sources, with optional Tavily search for alternative coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luogao2333](https://clawhub.ai/user/luogao2333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect current news lists, follow RSS sources, and expand selected items with full article retrieval or alternative free-source searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch public news pages and should not be aimed at private, localhost, intranet, or authenticated pages unless that access is intentional. <br>
Mitigation: Use it for public news sources by default and avoid private URLs or authenticated content in routine use. <br>
Risk: Optional Tavily search may send search queries to an external service. <br>
Mitigation: Use non-sensitive search terms and configure TAVILY_API_KEY only when external search is acceptable. <br>
Risk: News preferences may be saved in the workspace. <br>
Mitigation: Review or remove CONFIG/news-preferences.md when the saved preferences should not persist. <br>


## Reference(s): <br>
- [Free News Sources and RSS](references/free-sources.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/luogao2333/latte-news-fetcher-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown news digests with links, summaries, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local workspace preferences and optional Tavily search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
