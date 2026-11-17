## Description:

Interact with GitLab API for managing projects, issues, merge requests, branches, pipelines, users, groups, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonasgao](https://clawhub.ai/user/jonasgao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to let an agent operate against GitLab REST API v4 for repository, issue, merge request, branch, pipeline, group, user, label, milestone, release, snippet, search, runner, and webhook workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform write, delete, merge, pipeline, and webhook operations against real GitLab resources.

Mitigation: Use the least-privilege GitLab token that fits the task and require explicit user confirmation before destructive or state-changing operations.

Risk: Credential-safety gaps could expose or misuse a GitLab personal access token.

Mitigation: Keep GITLAB_TOKEN out of URLs and logs, set it manually in .env, and use read_api for read-only work.

Risk: A misconfigured GitLab endpoint could send authenticated requests to an untrusted server.

Mitigation: Configure only a trusted HTTPS GITLAB_URL before running gitlab-client commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jonasgao/skills/gitlab-api-client)
- [Publisher Profile](https://clawhub.ai/user/jonasgao)
- [GitLab REST API v4 Reference](https://gitlab.fullnine.com.cn/help/api/index.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from gitlab-client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITLAB_URL and a user-provided GITLAB_TOKEN in .env; API command output is JSON.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
