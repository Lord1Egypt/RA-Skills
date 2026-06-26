## Description: <br>
Work with GitHub repositories, issues, pull requests, commits, branches, releases, and workflows via the GitHub REST and GraphQL APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect and manage GitHub repositories, issues, pull requests, commits, branches, releases, and workflows through authenticated GitHub REST and GraphQL API tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth-backed access to GitHub resources available to the connected account. <br>
Mitigation: Use scoped credentials where possible and authorize only the GitHub account and repository access needed for the task. <br>
Risk: Repository, issue, pull request, release, workflow, or collaborator write actions can change external GitHub state. <br>
Mitigation: Preview and confirm the target resource and intended effect before executing any create, update, delete, workflow, or deployment action. <br>
Risk: Some GitHub tool calls may fail because of missing OAuth scopes, repository permissions, or rate limits. <br>
Mitigation: Verify the live GitHub connection and tool catalog before use, and report real API errors rather than assuming missing capability. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/github-repos) <br>
- [GitHub REST API Documentation](https://docs.github.com/en/rest) <br>
- [GitHub GraphQL API](https://docs.github.com/en/graphql) <br>
- [GitHub Actions Documentation](https://docs.github.com/en/actions) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct authenticated GitHub API tool calls through ClawLink after connection setup.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
