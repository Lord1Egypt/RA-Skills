## Description: <br>
Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phucanh08](https://clawhub.ai/user/phucanh08) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to construct public web searches across Chinese and global search engines, including site-specific queries, file-type searches, time filters, privacy-oriented engines, and WolframAlpha knowledge queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search providers may receive and retain user queries, including sensitive terms if the agent is prompted with them. <br>
Mitigation: Avoid passwords, tokens, confidential project names, customer data, regulated data, and unauthorized target queries when using the generated search URLs. <br>
Risk: Search-result guidance can be outdated, incomplete, or misleading because results depend on third-party search engines. <br>
Mitigation: Review retrieved results before acting on them and cross-check important findings against authoritative sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phucanh08/multi-search-engine-2) <br>
- [International search guide](references/international-search.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with URL examples and inline command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces search URL patterns and query-construction guidance; it does not require API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
