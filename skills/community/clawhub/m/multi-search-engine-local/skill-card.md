## Description: <br>
Multi search engine integration with 17 engines (8 CN + 9 Global), supporting advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reknottycat](https://clawhub.ai/user/reknottycat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to construct direct search URLs across Chinese and global search engines, including site-specific, filetype, time-filtered, privacy-focused, and WolframAlpha knowledge queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Advanced search operators could be used for credential discovery, admin endpoint hunting, recovering withdrawn sensitive content, or sending confidential queries to external search engines. <br>
Mitigation: Review and constrain agent use of the search templates; avoid sensitive queries and prohibit credential, admin endpoint, or withdrawn-content searches. <br>


## Reference(s): <br>
- [International Search Guide](references/international-search.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown with inline search URL and web_fetch examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces search-engine URL templates and query examples; no API keys are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
