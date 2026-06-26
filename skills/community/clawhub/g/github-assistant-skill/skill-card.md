## Description: <br>
A GitHub assistant skill for agents that can view Trending repositories, search projects, manage stars, forks, watches, issues, pull requests, code content, releases, Actions, users, notifications, organizations, and comments through the GitHub REST API and Playwright browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonforcode](https://clawhub.ai/user/leonforcode) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to browse GitHub Trending, search repositories and users, inspect repository content, and perform authenticated collaboration tasks such as issue, pull request, branch, release, workflow, star, fork, watch, notification, and organization operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad GitHub authority and can perform high-impact actions such as merges, workflow runs, file writes, repository creation, and settings access without strong built-in confirmation or scoping controls. <br>
Mitigation: Install only when you intend to let the agent act on your GitHub account. Use a fine-grained, short-lived token limited to selected repositories and the minimum permissions needed, and manually confirm high-impact actions before execution. <br>
Risk: Saved GitHub tokens and browser sessions can grant ongoing account access if exposed. <br>
Mitigation: Treat ~/.github-assistant/github_token.txt and ~/.github-assistant/github_auth.json as sensitive, avoid passing tokens on the command line when possible, and rotate or revoke credentials if they may have been exposed. <br>


## Reference(s): <br>
- [GitHub REST API Endpoints Reference](references/github_api_endpoints.md) <br>
- [GitHub-Assistant-Skill on ClawHub](https://clawhub.ai/leonforcode/github-assistant-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and text responses with command examples, GitHub data summaries, repository details, and operation status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default responses are documented as Chinese unless the user requests another language. Authenticated operations may call GitHub APIs or browser automation and can change repository or account state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
