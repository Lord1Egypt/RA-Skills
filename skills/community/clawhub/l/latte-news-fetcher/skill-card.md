## Description: <br>
Fetches current news, formats article lists, and helps agents retrieve article details using browser, search, archive, and text extraction services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luogao2333](https://clawhub.ai/user/luogao2333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect current news from preferred or specified sources, present categorized Markdown summaries, and retrieve article details when source access and configured tools allow it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes workflows for paywall circumvention and routing article URLs through third-party services. <br>
Mitigation: Install only where that behavior is acceptable; prefer free sources and review tool actions before execution. <br>
Risk: The skill may use logged-in browser sessions or personal news accounts to fetch article content. <br>
Mitigation: Avoid using a primary browser profile or logged-in accounts with this skill. <br>
Risk: Searches and article URLs can be sent to Tavily when TAVILY_API_KEY is configured. <br>
Mitigation: Leave TAVILY_API_KEY unset unless sharing those searches and URLs with Tavily is acceptable. <br>
Risk: Artifact guidance mentions changing privacy or network settings such as Private Relay or DNS. <br>
Mitigation: Do not change system privacy or DNS settings casually; use a separate environment or seek administrator review when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/luogao2333/latte-news-fetcher) <br>
- [Latte News Fetcher Homepage](https://github.com/luogao2333/Latte-news-fetcher) <br>
- [Professional News Website Resource List](references/news-sources.md) <br>
- [Free News Sources and RSS](references/free-sources.md) <br>
- [Paywall Difficulty Matrix](references/paywall-matrix.md) <br>
- [Bypass Tool Comparison](references/bypass-tools.md) <br>
- [Advanced Techniques and Tools](references/advanced-techniques.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown news lists, article summaries, configuration prompts, and occasional shell or API command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write CONFIG/news-preferences.md and may use TAVILY_API_KEY when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
