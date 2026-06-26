## Description: <br>
Linkup (linkup.so) helps an agent search the web, fetch webpages, produce sourced answers, return grounded search results, normalize structured data, and check credits through the OOMOL oo connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when an agent needs Linkup-backed web search, webpage extraction, sourced answers, structured search data, or credit-balance checks through an OOMOL-connected Linkup account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Linkup account and sensitive credentials managed through OOMOL. <br>
Mitigation: Use the OOMOL connection flow and avoid exposing raw API keys in prompts, shell history, or files. <br>
Risk: Web search and fetched webpage content can be incomplete, stale, or misleading. <br>
Mitigation: Review returned sources and verify important claims before relying on them for consequential decisions. <br>
Risk: First-time setup and billing errors may require user action before Linkup commands succeed. <br>
Mitigation: Only run authentication, connection, or billing setup steps after a matching command failure and with appropriate user confirmation. <br>


## Reference(s): <br>
- [Linkup homepage](https://www.linkup.so) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-linkup) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Linkup search answers, grounded result data, webpage markdown, optional raw HTML or image data, structured JSON data, and credit-balance information.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
