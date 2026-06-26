## Description: <br>
Upload images to img402.dev and return GitHub-ready Markdown links for PRs, issues, comments, and documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[img402](https://clawhub.ai/user/img402) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload screenshots, mockups, diagrams, and other visual artifacts so they can be embedded in GitHub pull requests, issues, comments, and documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images may contain tokens, private URLs, customer data, unreleased product details, or other information that should not leave the local environment or repository context. <br>
Mitigation: Inspect screenshots and mockups before upload and avoid sharing sensitive or private content. <br>
Risk: Hosted image links may be posted into GitHub PRs, issues, and comments where visibility can be broader than intended. <br>
Mitigation: Confirm the target repository, PR, issue, and audience before posting returned image markdown. <br>
Risk: Free-tier uploads expire after 7 days and are limited to 1 MB. <br>
Mitigation: Resize images before upload when needed and use the documented paid retention tier for durable documentation images. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/img402/github-image-hosting) <br>
- [img402.dev](https://img402.dev) <br>
- [img402 x402 API Payments](https://img402.dev/blog/paying-x402-apis) <br>
- [Coinbase Payments MCP](https://docs.cdp.coinbase.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and GitHub image markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hosted image URLs returned by img402.dev; free uploads are limited to 1 MB and 7-day retention.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
