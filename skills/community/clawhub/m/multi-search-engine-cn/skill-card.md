## Description: <br>
Multi Search Engine helps agents compose searches across 17 Chinese and global search engines with advanced operators, time filters, privacy-focused engines, and WolframAlpha knowledge queries without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to construct search queries across multiple search engines for web research, site-specific searches, file-type searches, time-filtered searches, privacy-focused searches, and knowledge queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search guidance can be misused to look for exposed passwords, admin pages, private files, or removed cached content. <br>
Mitigation: Use the skill only for legitimate web research and reject searches intended to discover credentials, private systems, or restricted content. <br>
Risk: Search queries may disclose secrets, personal data, internal domains, or confidential project names to third-party search engines. <br>
Mitigation: Do not include secrets, personal data, internal hostnames, or confidential project terms in queries; sanitize search terms before use. <br>


## Reference(s): <br>
- [International Search Guide](references/international-search.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jirboy/multi-search-engine-cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with search URL examples and web_fetch command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces query guidance and direct search URLs; no API keys are required by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact files list 2.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
