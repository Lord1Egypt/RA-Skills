## Description: <br>
Fast headless browser web scraping using Lightpanda for OSINT recon, link extraction, and content scraping without GPU or heavy browser dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hostilespider](https://clawhub.ai/user/hostilespider) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to scrape pages, extract links, save rendered page content, evaluate simple JavaScript, or expose Lightpanda through CDP or MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an unpinned native Lightpanda binary downloaded from GitHub. <br>
Mitigation: Install only when the Lightpanda project and release source are trusted, and review the install commands before execution. <br>
Risk: Options such as --js, --serve, --mcp, --proxy, and --output enable powerful browser automation, network routing, server mode, and file-writing behavior. <br>
Mitigation: Review commands before running them, stop server modes when finished, and avoid scraping or storing data without authorization. <br>


## Reference(s): <br>
- [Lightpanda browser repository](https://github.com/nicholasgasior/lightpanda-browser) <br>
- [Lightpanda Linux x86_64 release binary](https://github.com/nicholasgasior/lightpanda-browser/releases/latest/download/lightpanda-linux-x86_64) <br>
- [ClawHub skill page](https://clawhub.ai/hostilespider/lightpanda-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/hostilespider) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, raw HTML, plain text link lists, JSON values from JavaScript evaluation, shell commands, and saved files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write scraped output to a user-specified file and can start long-running CDP or MCP server modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
