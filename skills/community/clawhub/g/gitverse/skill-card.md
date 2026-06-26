## Description: <br>
GitVerse API integration for working with repositories, issues, and pull requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webchi](https://clawhub.ai/user/webchi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent inspect GitVerse repositories, issues, pull requests, comments, commits, and changed files, and to create pull requests when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The GitVerse token can provide real account and repository access. <br>
Mitigation: Use a token with the smallest needed scope and keep environment files out of commits and shared locations. <br>
Risk: Pull request creation can affect repository workflows. <br>
Mitigation: Confirm the repository owner, repository name, title, head branch, and base branch before creating a pull request. <br>
Risk: A custom GITVERSE_BASE_URL can send authenticated requests to a non-default endpoint. <br>
Mitigation: Leave GITVERSE_BASE_URL unset unless the endpoint is intentionally configured and trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/webchi/gitverse) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON] <br>
**Output Format:** [JSON emitted to stdout from CLI commands, with errors emitted to stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GITVERSE_TOKEN; uses https://gitverse.ru/api/v1 unless GITVERSE_BASE_URL is intentionally set.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
