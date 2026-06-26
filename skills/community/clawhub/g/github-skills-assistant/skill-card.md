## Description: <br>
Query and manage GitHub repositories, including listing repositories, checking CI status, creating issues, searching repositories, and viewing recent activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesong-hue](https://clawhub.ai/user/yesong-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and GitHub users use this skill to let an assistant retrieve repository information, inspect CI and recent activity, and initiate GitHub write actions such as creating issues or repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured GitHub token can permit lasting read and write actions, including issue, repository, or pull request creation. <br>
Mitigation: Use a narrowly scoped token, avoid full private-repository access unless needed, review token storage, and manually confirm write actions before allowing them to run. <br>
Risk: The security summary notes an under-documented pull request action without built-in confirmation. <br>
Mitigation: Require explicit human approval before pull request creation and document the expected owner, repository, branch, and title inputs before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yesong-hue/github-skills-assistant) <br>
- [GitHub personal access tokens](https://github.com/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration guidance] <br>
**Output Format:** [Text responses with repository, CI, issue, pull request, or activity data returned through the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GitHub credentials via GITHUB_TOKEN and GITHUB_USERNAME environment variables or github.token and github.username configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
