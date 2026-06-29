## Description: <br>
GitHub API integration with managed OAuth for accessing repositories, issues, pull requests, commits, branches, and users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to work with GitHub repositories, issues, pull requests, commits, branches, users, and search through Maton-managed OAuth access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill brokers GitHub access through Maton OAuth/API access. <br>
Mitigation: Install only if the publisher and Maton OAuth brokerage are trusted, and confirm the intended GitHub account connection before use. <br>
Risk: GitHub write operations can create, update, merge, delete, transfer, or otherwise change repository resources. <br>
Mitigation: Before writes, confirm the exact repository, account connection, target object, and whether the action is reversible. <br>
Risk: Some operations such as merges, deletes, branch changes, collaborator changes, and organization-level actions have elevated impact. <br>
Mitigation: Require explicit user approval and extra confirmation for high-impact or organization-level actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/skills/github-api) <br>
- [GitHub REST API Documentation](https://docs.github.com/en/rest) <br>
- [GitHub Repositories API](https://docs.github.com/en/rest/repos/repos) <br>
- [GitHub Issues API](https://docs.github.com/en/rest/issues/issues) <br>
- [GitHub Pull Requests API](https://docs.github.com/en/rest/pulls/pulls) <br>
- [GitHub Search API](https://docs.github.com/en/rest/search/search) <br>
- [GitHub Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>
- [Maton API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce GitHub API paths, Maton CLI commands, request examples, OAuth connection guidance, and cautions for write operations.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
