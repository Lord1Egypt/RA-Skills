## Description: <br>
Crawl web pages and detect broken links, redirects, and HTTP errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site maintainers, and content teams use this skill to audit URLs, scan documents for broken links, review redirect and HTTP error status, and export link-checking reports before or after publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checked URLs are contacted over the network, which can expose private, internal, or token-bearing URLs to remote servers. <br>
Mitigation: Avoid scanning private files, internal endpoints, or URLs containing secrets unless that exposure is acceptable. <br>
Risk: Full checked URLs are saved locally in history, reports, and exports under ~/.link-checker. <br>
Mitigation: Delete local history, reports, or exports after use when URLs are sensitive. <br>


## Reference(s): <br>
- [BytesAgain](https://bytesagain.com) <br>
- [Link Checker on ClawHub](https://clawhub.ai/xueyetianya/link-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and text, CSV, JSON, or TXT report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl-based HTTP checks, stores local history and reports under ~/.link-checker, and supports timeout, retry, and user-agent configuration.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
