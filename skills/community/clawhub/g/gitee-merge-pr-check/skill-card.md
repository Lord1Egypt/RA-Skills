## Description: <br>
Checks whether a Gitee pull request is ready to merge and, after explicit confirmation, can merge it through a configured Gitee MCP Server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oschina](https://clawhub.ai/user/oschina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to evaluate Gitee pull request readiness by checking PR status, reviewer feedback, comments, and changed files before deciding whether to merge. When checks pass, the skill asks for explicit confirmation before using the configured Gitee MCP Server to merge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform a repository merge through the configured Gitee MCP Server, which can change the target repository history. <br>
Mitigation: Confirm the repository, PR number, merge method, account permissions, and explicit user approval before approving a merge. <br>
Risk: The skill depends on Gitee MCP access to inspect PR details, comments, diffs, and merge status. <br>
Mitigation: Install it only in environments where the agent is allowed to use the configured Gitee MCP Server for PR review and merging. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown merge-readiness report with confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires repository owner, repository name, PR number, and access to a configured Gitee MCP Server.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
