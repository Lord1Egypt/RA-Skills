## Description: <br>
Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Djttt](https://clawhub.ai/user/Djttt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose search engines, compose advanced search queries, and issue web_fetch calls across Chinese and global search providers without API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may disclose secrets, credentials, confidential project terms, private names, or sensitive personal searches to external search providers. <br>
Mitigation: Do not use the skill with sensitive query terms unless the user has accepted disclosure to the selected provider. <br>
Risk: Search providers can return unsafe, irrelevant, or misleading results, and some queries may disable or weaken safe-search protections. <br>
Mitigation: Keep safe-search enabled unless deliberately needed, and review search results before relying on them or passing them into downstream workflows. <br>


## Reference(s): <br>
- [International Search Guide](references/international-search.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Djttt/openclaw-multi-search-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown with JavaScript web_fetch examples and search URL patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys required; using the generated search URLs sends query text to external search providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact files reference 2.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
