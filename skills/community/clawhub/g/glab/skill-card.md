## Description: <br>
GitLab CLI for managing issues, merge requests, CI/CD pipelines, and repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bezkom](https://clawhub.ai/user/bezkom) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to operate GitLab workflows from the command line, including merge requests, issues, CI/CD pipelines, self-hosted GitLab instances, and automation scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad GitLab token can permit destructive repository, project, issue, merge request, or API actions. <br>
Mitigation: Use the least-privileged GitLab token that fits the task, prefer read_api for read-only work, and review write or delete operations before running them. <br>
Risk: The glab api command can use the authenticated token for broad GitLab REST API access. <br>
Mitigation: Dry-run with read requests where possible, limit token scope, and inspect POST, PUT, or DELETE API calls before execution. <br>
Risk: GitLab tokens can be exposed through terminal output, logs, screenshots, or support requests. <br>
Mitigation: Do not print or share the full GITLAB_TOKEN, redact sensitive values from diagnostics, and rotate any token that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bezkom/glab) <br>
- [Advanced API Access](references/api-advanced.md) <br>
- [Detailed Command Reference](references/commands-detailed.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [GitLab REST API](https://docs.gitlab.com/ee/api/) <br>
- [GitLab CLI documentation](https://docs.gitlab.com/editor_extensions/gitlab_cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include executable shell commands that require glab, jq, GitLab credentials, and repository context.] <br>

## Skill Version(s): <br>
1.0.4 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
