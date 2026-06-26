## Description: <br>
Provides reusable guidance and URL patterns for agents to query 17 Chinese and global search engines with advanced operators, time filters, privacy-focused engines, and WolframAlpha queries without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelaner](https://clawhub.ai/user/kelaner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to construct search queries across multiple search engines, including site-specific search, filetype search, time filters, privacy-oriented search providers, and WolframAlpha knowledge queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to external search engines and may expose sensitive terms. <br>
Mitigation: Do not include passwords, tokens, personal identifiers, confidential business information, or other sensitive data in search queries. <br>
Risk: Advanced search operators can surface content outside the user's intended scope. <br>
Mitigation: Use advanced operators only for authorized research and review generated search URLs before fetching results. <br>


## Reference(s): <br>
- [International Search Guide](references/international-search.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kelaner/multi-search-engine-tmp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with URL examples and web_fetch command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys required; query handling depends on the selected external search engine.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact changelog top entry is 2.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
