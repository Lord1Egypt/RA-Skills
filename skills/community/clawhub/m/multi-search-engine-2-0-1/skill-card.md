## Description: <br>
Multi search engine integration with 17 engines (8 CN + 9 Global), advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomon4github](https://clawhub.ai/user/solomon4github) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to assemble web search URLs across Chinese and global search engines, including site-specific searches, file-type searches, time filters, privacy-oriented engines, DuckDuckGo bangs, and WolframAlpha knowledge queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are submitted to third-party public search engines and may expose sensitive terms. <br>
Mitigation: Avoid searching for secrets, credentials, private business terms, or regulated personal data. <br>
Risk: Search options can surface explicit, inappropriate, or misleading public results. <br>
Mitigation: Review returned results before relying on them and use safe-search or narrower query filters when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solomon4github/multi-search-engine-2-0-1) <br>
- [International Search Guide](references/international-search.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown with search URL templates and web_fetch examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys are required; generated queries are sent to third-party public search engines selected by the user.] <br>

## Skill Version(s): <br>
ClawHub release 1.0.0; skill content v2.0.1 (sources: evidence release metadata, artifact metadata, and changelog released 2026-02-06) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
