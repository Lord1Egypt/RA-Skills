## Description: <br>
Use this skill when the user asks to review a PR, do a code review, check a pull request, "review this PR", "review-pr", or "look at this pull request". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oschina](https://clawhub.ai/user/oschina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Gitee pull requests by inspecting PR details, changed files, existing comments, and review dimensions such as correctness, security, maintainability, performance, and consistency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish a Gitee pull request comment through the user's configured MCP account without first requiring approval. <br>
Mitigation: Ask the agent to draft the review in chat first, confirm the repository and PR number, and approve the exact text before allowing comment_pull. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oschina/gitee-review-pr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review comments and concise review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May post review comments to a Gitee pull request through the configured Gitee MCP account.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
