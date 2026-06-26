## Description: <br>
GitHub API integration with managed OAuth for accessing repositories, issues, pull requests, commits, branches, users, and search workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to interact with GitHub through Maton-managed OAuth, including repository, issue, pull request, branch, commit, organization, and search operations. It is suited for GitHub workflow automation where the user can approve write operations and provide a valid Maton API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials and a managed GitHub OAuth connection. <br>
Mitigation: Use least-privilege OAuth scopes, protect MATON_API_KEY from logs and chat, and install only if the publisher is trusted with the connected GitHub accounts and repositories. <br>
Risk: Repository-changing operations can create, update, delete, merge, transfer, or otherwise alter GitHub resources. <br>
Mitigation: Confirm the exact target, verify the intended connection ID when multiple accounts exist, and state whether the action is reversible or destructive before approval. <br>
Risk: Irreversible or high-impact operations such as deleting repositories, rewriting history, merging pull requests, removing collaborators, or transferring ownership can be difficult or impossible to undo. <br>
Mitigation: Require explicit user confirmation and extra caution for these operations, and keep actions limited to repositories and organizations the user names for the current task. <br>


## Reference(s): <br>
- [ClawHub GitHub Skill](https://clawhub.ai/byungkyu/github-api) <br>
- [GitHub REST API Documentation](https://docs.github.com/en/rest) <br>
- [GitHub Repositories API](https://docs.github.com/en/rest/repos/repos) <br>
- [GitHub Issues API](https://docs.github.com/en/rest/issues/issues) <br>
- [GitHub Pull Requests API](https://docs.github.com/en/rest/pulls/pulls) <br>
- [GitHub Search API](https://docs.github.com/en/rest/search/search) <br>
- [GitHub REST API Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API calls] <br>
**Output Format:** [Markdown with REST endpoint examples, CLI commands, and Python or JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected GitHub OAuth account.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
