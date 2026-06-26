## Description: <br>
Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to choose public search engines and compose advanced web search queries, including site-specific searches, time filters, privacy-oriented engines, and WolframAlpha knowledge lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries sent to public search engines may expose confidential terms, private project names, internal URLs, credentials, or customer data. <br>
Mitigation: Do not include passwords, tokens, customer data, internal URLs, private project names, or confidential research terms in queries. <br>
Risk: Advanced search examples involving passwords, admin pages, cached pages, or financial topics can be misused outside authorized research. <br>
Mitigation: Use these examples only for authorized research and review generated queries before opening or fetching results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/multi-search-engine-litiao) <br>
- [litiao1224 publisher profile](https://clawhub.ai/user/litiao1224) <br>
- [International search guide](references/international-search.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with inline web_fetch examples and search URL templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys required; search behavior depends on the selected public search engine.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact documentation cites v2.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
