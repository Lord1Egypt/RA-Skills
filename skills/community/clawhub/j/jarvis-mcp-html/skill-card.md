## Description:

Jarvis MCP HTML Extractor helps agents extract text, links, and JSON API content from web pages through mcporter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claudedamir-art](https://clawhub.ai/user/claudedamir-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to install and call an MCP HTML extraction server for web scraping tasks, including fetching pages, extracting text and links, and calling JSON APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external npm package installed at runtime.

Mitigation: Confirm the npm package and publisher are trusted, and consider pinning a reviewed package version before use.

Risk: The MCP server fetches user-supplied URLs, which can create outbound web request and internal network exposure concerns.

Mitigation: Run the skill in an environment where outbound requests cannot reach sensitive internal systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claudedamir-art/skills/jarvis-mcp-html)
- [npm package](https://npm.im/html-extractor-mcp)
- [ClawHub publisher profile](https://clawhub.ai/user/claudedamir-art)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and html-extractor-mcp binaries; MCP calls may make outbound requests to user-supplied URLs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
