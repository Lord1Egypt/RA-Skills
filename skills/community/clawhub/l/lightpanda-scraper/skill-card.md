## Description:

Fast headless browser web scraping using Lightpanda for OSINT recon, link extraction, and content scraping without GPU or heavy browser dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hostilespider](https://clawhub.ai/user/hostilespider)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and security practitioners use this skill to run fast headless browser scraping, extract links, save page content, evaluate simple JavaScript, or start Lightpanda CDP/MCP modes for authorized web analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unverified third-party native Lightpanda binary that may change after review.

Mitigation: Use a pinned Lightpanda release and verify its SHA-256 checksum or signature before installation.

Risk: Scraping can access sites or content outside the user's authorization.

Mitigation: Use the scraper only on sites and paths the user is authorized to access, and follow applicable site terms and legal requirements.

Risk: Saved scrape output may contain sensitive local data.

Mitigation: Store output only where appropriate, protect files containing sensitive content, and delete scrape artifacts when they are no longer needed.

## Reference(s):

- [Lightpanda project](https://github.com/nicholasgasior/lightpanda-browser)
- [Lightpanda Linux x86_64 release asset](https://github.com/nicholasgasior/lightpanda-browser/releases/latest/download/lightpanda-linux-x86_64)
- [ClawHub skill page](https://clawhub.ai/hostilespider/skills/lightpanda-scraper)
- [ClawHub publisher profile](https://clawhub.ai/user/hostilespider)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, raw HTML, JSON values, newline-delimited links, shell commands, or saved local files depending on selected options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write scrape output to a local file and can start Lightpanda CDP or MCP server modes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
