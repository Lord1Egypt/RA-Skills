## Description:

Work with GitLab projects, issues, merge requests, commits, branches, pipelines, and groups through the GitLab API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw to GitLab through ClawLink, inspect GitLab resources, and perform confirmed write actions such as creating issues or managing projects, members, branches, and pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth-backed GitLab access can expose sensitive project data or permit actions within the connected account's permissions.

Mitigation: Use a least-privileged GitLab account or scopes where possible, verify the GitLab connection before use, and review requested tool actions before execution.

Risk: Create, update, delete, member-management, and CI/CD pipeline operations can change repositories, permissions, or build and deployment state.

Mitigation: Prefer read, list, search, and describe operations before writes; preview write actions and confirm the target resource and intended effect with the user.

Risk: The artifact labels project archival as read-only even though archiving is state-changing.

Mitigation: Treat archive operations as write actions and require explicit confirmation before execution.

## Reference(s):

- [ClawHub GitLab skill page](https://clawhub.ai/hith3sh/skills/gitlab-repos)
- [GitLab API Documentation](https://docs.gitlab.com/api/)
- [GitLab REST API](https://docs.gitlab.com/api/rest.html)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=gitlab-repos)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ClawLink plugin and a connected GitLab account; write operations require preview and explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
