## Description: <br>
Guides an agent through implementing a Gitee issue by fetching issue context, analyzing requirements, making code changes, creating a pull request, and updating the issue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oschina](https://clawhub.ai/user/oschina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to implement Gitee issues from a local repository checkout, including issue analysis, code-change guidance, pull request creation, and issue follow-up through a configured Gitee MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post issue comments, create pull requests, and update issue status through Gitee. <br>
Mitigation: Use a least-privilege Gitee MCP account and review generated comments, pull request text, and issue status changes before submission. <br>
Risk: Using the wrong local checkout could lead the agent to modify or propose changes for the wrong repository. <br>
Mitigation: Confirm the repository owner, repository name, issue number, and local repository path before implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oschina/gitee-implement-issue) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown text with issue analysis, implementation guidance, issue comments, pull request descriptions, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Gitee MCP server and a local checkout of the target repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
