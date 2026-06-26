## Description: <br>
Multi search engine integration with 16 engines (7 CN + 9 Global), advanced search operators, time filters, site search, privacy-focused engines, and WolframAlpha knowledge queries without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcdentoncore](https://clawhub.ai/user/jcdentoncore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose among Chinese and global search engines, issue targeted web search requests, and aggregate results into concise search reports. It is useful for advanced operators, time filters, site-specific search, privacy-oriented search providers, and WolframAlpha-style knowledge queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and URLs are sent to third-party search engines even when execution is local. <br>
Mitigation: Avoid secrets, personal data, private identifiers, and sensitive research terms unless disclosure to the selected providers is acceptable. <br>
Risk: Automatic provider selection may route a query to a provider the user did not intend to use. <br>
Mitigation: Prefer explicit provider selection for sensitive or jurisdiction-dependent searches. <br>
Risk: Cached or deleted-content searches and safe-search-disabling examples may surface material that requires special care. <br>
Mitigation: Require clear user intent before using those operators and review the resulting content before reuse. <br>
Risk: Direct search aggregation can trigger provider rate limits or terms-of-service issues. <br>
Mitigation: Use the documented delays, small batches, and single retry behavior, and respect each search engine's policies. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jcdentoncore/multi-search-engine-2-1-3) <br>
- [Domestic search guide](artifact/references/advanced-search.md) <br>
- [International search guide](artifact/references/international-search.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown search report with inline web_fetch request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include direct search-engine URLs, provider selection notes, retry guidance, and concise result summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata also references 2.1.3 and changelog references v2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
