## Description: <br>
GitHub team collaboration toolkit for managing team workflows, code reviews, issue tracking, sprint planning, and team metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate GitHub repository work, automate pull request and issue workflows, track milestone progress, and analyze collaboration metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a GitHub token for repository actions that can modify repository state. <br>
Mitigation: Use a fine-grained GitHub token with only the repository permissions needed and require explicit confirmation before write actions. <br>
Risk: Running the module directly can partially print the configured GitHub token prefix. <br>
Mitigation: Avoid running the module entry point until token-prefix printing is removed, and keep tokens out of logs and shared terminal output. <br>
Risk: Automated issue and pull request operations can make unintended changes if called with incorrect repository, issue, or reviewer parameters. <br>
Mitigation: Review target owner, repository, pull request, issue, labels, assignees, and reviewer inputs before executing write-capable functions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/github-team-collaboration) <br>
- [Publisher Profile](https://clawhub.ai/user/kaiyuelv) <br>
- [GitHub REST API](https://api.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a GITHUB_TOKEN environment variable and may return GitHub API JSON dictionaries or error dictionaries from helper functions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
