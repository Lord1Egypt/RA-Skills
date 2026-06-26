## Description: <br>
Search GitHub repos, view issues, and look up user profiles via the public REST API; no token required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to search public GitHub repositories, inspect repository metadata and issues, and look up public GitHub user profiles through Pipeworx. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public GitHub lookup queries are sent through Pipeworx. <br>
Mitigation: Avoid entering confidential repository names, private investigation terms, or sensitive business context into queries. <br>
Risk: The optional MCP configuration uses mcp-remote@latest. <br>
Mitigation: Pin mcp-remote to a reviewed version when using the optional MCP configuration. <br>
Risk: Unauthenticated GitHub API requests are limited to 60 requests per hour per IP. <br>
Mitigation: Plan low-volume public lookups for this skill or use authenticated GitHub access through another approved path for heavier use. <br>


## Reference(s): <br>
- [Pipeworx GitHub Pack](https://pipeworx.io/packs/github) <br>
- [Pipeworx GitHub MCP Endpoint](https://gateway.pipeworx.io/github/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/pipeworx-github) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown/text with JSON MCP configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Public GitHub lookup results may include repository names, descriptions, stars, forks, language, license, issue metadata, user profile fields, and URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
