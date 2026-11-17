## Description:

Manage GitLab repositories, merge requests, and issues via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jorgermp](https://clawhub.ai/user/jorgermp)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to automate common GitLab tasks, including creating repositories, listing merge requests, commenting on merge requests, and creating issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated commands can create repositories, create issues, or post merge request comments in unintended GitLab resources.

Mitigation: Use a narrowly scoped project or group token, avoid broad personal tokens, and verify command arguments before execution.

Risk: Weak input validation can make malformed or unintended GitLab API requests more likely.

Mitigation: Review project paths, issue titles, merge request IDs, and comment bodies before running the script, especially in production namespaces.

## Reference(s):

- [GitLab API v4](https://gitlab.com/api/v4)
- [ClawHub skill page](https://clawhub.ai/jorgermp/skills/gitlab-manager)
- [Publisher profile](https://clawhub.ai/user/jorgermp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash code blocks and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GitLab API responses and requires GITLAB_TOKEN for authenticated operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
