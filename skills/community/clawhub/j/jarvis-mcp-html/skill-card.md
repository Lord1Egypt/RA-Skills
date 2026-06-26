## Description: <br>
Provides an MCP server for HTML extraction and web scraping through mcporter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudedamir-art](https://clawhub.ai/user/claudedamir-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch web pages, extract text and links, and call JSON APIs through the html-extractor-mcp MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs network fetching, which can expose internal, authenticated, localhost, or policy-restricted URLs if an agent is allowed to request them. <br>
Mitigation: Use it only for URLs the agent is trusted to fetch, avoid restricted sites unless explicitly intended, and test or pin the npm package in an isolated environment before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/claudedamir-art/jarvis-mcp-html) <br>
- [html-extractor-mcp package](https://npm.im/html-extractor-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and MCP call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses stdio on demand and requires the mcporter and html-extractor-mcp binaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
