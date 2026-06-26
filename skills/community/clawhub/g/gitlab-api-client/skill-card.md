## Description: <br>
Interact with GitLab API for managing projects, issues, merge requests, branches, pipelines, users, groups, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonasgao](https://clawhub.ai/user/jonasgao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and GitLab administrators use this skill to let an agent query and manage GitLab projects, issues, merge requests, branches, repositories, pipelines, groups, users, labels, milestones, tags, releases, snippets, runners, and webhooks through GitLab REST API v4. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad GitLab write, delete, merge, approve, retry, cancel, and webhook authority through the provided token. <br>
Mitigation: Use a read-only or narrowly scoped token when possible, and require explicit confirmation of exact project IDs, branches, files, issues, merge requests, pipeline IDs, and webhook URLs before any mutating action. <br>
Risk: The GitLab token can be exposed if it is printed, placed in URLs, or committed with environment files. <br>
Mitigation: Do not print or echo GITLAB_TOKEN, do not put tokens in URLs, keep .env out of version control, and have the user set the token manually. <br>


## Reference(s): <br>
- [GitLab REST API v4 Reference Manual](https://gitlab.fullnine.com.cn/help/api/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with gitlab-client shell commands; command output is JSON or plain text for raw logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GITLAB_URL and GITLAB_TOKEN in .env; list operations support pagination.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
