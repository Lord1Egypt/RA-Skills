## Description: <br>
GitHub 操作工具 - 通过 GitHub API 管理仓库、Issues、PRs、Actions 等 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to draft and run GitHub REST API workflows for repositories, issues, pull requests, commits, Actions, search, files, and user information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide state-changing GitHub actions such as creating or closing issues, creating or merging pull requests, adding labels, assigning users, and dispatching workflows. <br>
Mitigation: Review proposed GitHub writes before execution and use a token scoped only to the repositories and operations needed. <br>
Risk: GitHub token exposure would grant access according to the token's configured permissions. <br>
Mitigation: Store GITHUB_TOKEN in environment or agent configuration, avoid hardcoding it in commands or files, and redact it from logs and shared transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaoren36-arch/github-api-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a GITHUB_TOKEN environment variable for authenticated GitHub REST API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
