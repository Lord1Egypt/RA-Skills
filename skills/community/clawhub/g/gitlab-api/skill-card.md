## Description: <br>
GitLab API integration for repository operations. Use when working with GitLab repositories for reading, writing, creating, or deleting files, listing projects, managing branches, or any other GitLab repository operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d1gl3](https://clawhub.ai/user/d1gl3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure GitLab API access and perform GitLab repository operations such as listing projects, reading and writing files, deleting files, listing directories, and managing branches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a GitLab token to read or modify repositories, including write and delete operations. <br>
Mitigation: Use a dedicated least-privilege token, prefer read-only scopes unless writes are required, and manually confirm the target project, branch, path, and commit details before write or delete operations. <br>
Risk: Token files and instance configuration can expose repository access if stored or pointed at untrusted locations. <br>
Mitigation: Protect token files with restrictive permissions and configure only trusted HTTPS GitLab instances. <br>


## Reference(s): <br>
- [GitLab API resources](https://docs.gitlab.com/ee/api/api_resources.html) <br>
- [GitLab personal access tokens](https://gitlab.com/-/user_settings/personal_access_tokens) <br>
- [ClawHub release page](https://clawhub.ai/d1gl3/gitlab-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash code blocks and shell script examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided GitLab token and a GitLab instance URL; supports GitLab.com and self-hosted GitLab instances.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
