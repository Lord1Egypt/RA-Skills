## Description: <br>
Searches Gitee for open source repositories that match a user's criteria, compares candidates, and forks the selected repository through the configured Gitee MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oschina](https://clawhub.ai/user/oschina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to discover relevant open source projects on Gitee, compare repository quality and activity, and fork a selected project into their Gitee account for evaluation or contribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can fork a repository into the user's Gitee account after a selection is made. <br>
Mitigation: Confirm the exact source repository and destination account or organization before invoking the fork operation. <br>
Risk: Repository search results may include unsuitable licenses or unmaintained projects. <br>
Mitigation: Compare activity, maintenance signals, documentation, and license terms before recommending or forking a candidate. <br>
Risk: The skill depends on credentials available through the configured Gitee MCP account. <br>
Mitigation: Use least-privileged Gitee credentials appropriate for repository discovery and forking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oschina/gitee-search-and-fork) <br>
- [Publisher profile](https://clawhub.ai/user/oschina) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance, API Calls] <br>
**Output Format:** [Markdown with repository recommendations, rationale, fork results, and suggested shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Gitee MCP server and user confirmation before forking a repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
