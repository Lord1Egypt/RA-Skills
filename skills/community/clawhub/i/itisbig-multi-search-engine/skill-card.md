## Description: <br>
Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasdkc](https://clawhub.ai/user/jasdkc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to search current public web information across Chinese and global search engines, including news, academic sources, privacy-oriented engines, site searches, time-filtered searches, and WolframAlpha knowledge queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to external search engines and may expose secrets, personal data, internal identifiers, or confidential business content. <br>
Mitigation: Use the skill only for public or approved queries, and do not include passwords, tokens, private records, sensitive personal details, internal identifiers, or confidential business content in search terms. <br>
Risk: Optional API keys for Google, Bing, or WolframAlpha can be exposed if stored or shared carelessly. <br>
Mitigation: Provide API keys only when needed, keep them restricted to the minimum required scope, store them in protected local configuration, and rotate them if exposure is suspected. <br>
Risk: Advanced search examples can be used for sensitive discovery patterns such as finding login pages or exposed files. <br>
Mitigation: Use advanced operators only for legitimate, authorized research and review queries before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jasdkc/itisbig-multi-search-engine) <br>
- [International Search Guide](references/international-search.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples, plus JSON search result objects containing title, URL, snippet, engine, and position fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include search engine selection, count limits, time filters, site-specific search, optional API-key configuration, and advanced search operator examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata; artifact files also mention 2.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
