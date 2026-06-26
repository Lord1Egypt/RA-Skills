## Description: <br>
Aggregates unread Gitee notifications, pending pull requests, and open issues into a daily work digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oschina](https://clawhub.ai/user/oschina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to summarize their Gitee work queue, including unread notifications, review requests, pending pull requests, and open issues. It helps prioritize daily follow-up across repositories accessible through the configured Gitee MCP Server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Gitee account notifications, pull requests, issues, and profile data through the configured MCP server. <br>
Mitigation: Use it only with Gitee MCP server scopes and repositories that are appropriate to summarize in chat. <br>
Risk: Broad activation wording can cause the skill to run for general daily-planning requests. <br>
Mitigation: Prefer explicit requests such as "show my Gitee daily digest" when account data should be read. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown daily digest with grouped notifications, pull request tables, issue tables, and prioritized suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Gitee MCP Server with access to the relevant account and repositories.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
