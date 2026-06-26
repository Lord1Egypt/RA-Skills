## Description: <br>
Fetch and query GitCode REST API data for repositories, branches, issues, pull requests, commits, tags, users, organizations, search, webhooks, members, releases, and related GitCode resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autoxj](https://clawhub.ai/user/autoxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up GitCode API paths, authentication requirements, status codes, and examples for repository, issue, pull request, commit, organization, member, webhook, and release workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated GitCode API examples may guide an agent toward actions that create issues or pull requests, change files or settings, manage webhooks, transfer or delete repositories, or add and remove members. <br>
Mitigation: Require explicit user approval before any operation that changes repository content, settings, access, webhooks, issues, pull requests, releases, or membership. <br>
Risk: GitCode tokens can expose private repositories or allow write actions depending on granted scopes. <br>
Mitigation: Use a least-privilege token through GITCODE_TOKEN, avoid long-lived tokens in chat or URLs, and rotate credentials if they are exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/autoxj/gitcode) <br>
- [GitCode API documentation](https://docs.gitcode.com/docs/apis/) <br>
- [reference.md](artifact/reference.md) <br>
- [examples.md](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with REST API paths, authentication notes, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GitCode token for authenticated endpoints; token may be supplied by the user or via GITCODE_TOKEN.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
