## Description: <br>
Searches the live web for current, citable information across news, research, documentation, company and market research, and fact-checking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keenable](https://clawhub.ai/user/keenable) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to retrieve current web results, source URLs, and snippets for research, news lookup, fact-checking, documentation discovery, and market research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Keenable's public search endpoint. <br>
Mitigation: Do not include secrets, credentials, private customer data, or confidential business material in queries. <br>
Risk: An agent may auto-route broad search requests to this skill. <br>
Mitigation: Use explicit Keenable-specific invocation when routing should be controlled. <br>
Risk: The public endpoint may rate-limit requests. <br>
Mitigation: Retry later when a rate-limit response is returned. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/keenable/skills/keenable-web-search) <br>
- [Keenable](https://keenable.ai) <br>
- [Keenable Public Search Endpoint](https://api.keenable.ai/v1/search/public) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Formatted text search results with titles, URLs, and snippets, or raw JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports natural-language queries plus optional site and date filters; public endpoint responses may be rate-limited.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
