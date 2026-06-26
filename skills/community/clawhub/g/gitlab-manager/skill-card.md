## Description: <br>
Manage GitLab repositories, merge requests, and issues via API. Use for tasks like creating repos, reviewing code in MRs, or tracking issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jorgermp](https://clawhub.ai/user/jorgermp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to manage GitLab projects, merge requests, and issues from an agent workflow, including creating repositories, listing or commenting on merge requests, and creating issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A GitLab token with broad permissions could allow unintended repository, merge request, or issue changes. <br>
Mitigation: Use a dedicated least-privilege GitLab token limited to the relevant projects or groups. <br>
Risk: Write actions can create repositories, create issues, or post merge request comments in GitLab. <br>
Mitigation: Review proposed commands, target project paths, and write-action arguments before execution. <br>


## Reference(s): <br>
- [Gitlab Manager on ClawHub](https://clawhub.ai/jorgermp/gitlab-manager) <br>
- [GitLab REST API v4 endpoint](https://gitlab.com/api/v4) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON or text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GITLAB_TOKEN environment variable with appropriate GitLab API permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
