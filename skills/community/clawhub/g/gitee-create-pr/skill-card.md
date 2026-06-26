## Description: <br>
Creates structured Gitee pull requests by gathering branch and repository details, analyzing branch differences, drafting a Conventional Commits title and Markdown body, and submitting the PR through a configured Gitee MCP Server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oschina](https://clawhub.ai/user/oschina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to create Gitee pull requests with a clear title, structured description, testing notes, and optional issue-closing text. It is intended for workflows where a configured Gitee MCP Server can compare branches and create the PR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a real Gitee pull request using the user's configured access. <br>
Mitigation: Before creation, review the owner, repository, source branch, target branch, title, body, and any issue-closing text. <br>
Risk: A broad or misconfigured Gitee token could allow unintended repository changes through the MCP setup. <br>
Mitigation: Install and run the skill only with a trusted Gitee MCP configuration and appropriately scoped credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oschina/gitee-create-pr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown PR title and body plus a pull request link after creation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include issue-closing text when the user provides a linked issue number.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
