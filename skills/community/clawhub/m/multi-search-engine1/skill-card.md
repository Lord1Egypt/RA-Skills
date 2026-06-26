## Description: <br>
Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp33333333333](https://clawhub.ai/user/cp33333333333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to construct public web search requests across Chinese and global engines, including advanced operators, time filters, privacy-oriented engines, and WolframAlpha knowledge queries without API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to third-party public search providers. <br>
Mitigation: Do not search for secrets, personal data, confidential project names, credentials, or regulated information. <br>
Risk: Advanced search operators can be misused outside legitimate research workflows. <br>
Mitigation: Use site, file type, exact match, exclusion, and related operators only for authorized research and review queries before sending them. <br>


## Reference(s): <br>
- [International Search Guide](references/international-search.md) <br>
- [Version History](CHANGELOG.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cp33333333333/multi-search-engine1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with URL templates and JavaScript web_fetch examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys are required; search terms are sent to the selected public search provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact metadata and changelog list 2.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
