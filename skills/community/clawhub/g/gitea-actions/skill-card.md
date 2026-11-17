## Description:

Trigger workflows, list runs, and get status for Gitea/Forgejo Actions workflows using owner, repo, and workflow details via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhou-guo](https://clawhub.ai/user/qizhou-guo)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to trigger Gitea or Forgejo Actions workflows and inspect workflow run status from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Gitea API token can trigger workflows and read workflow-run information, so an overly broad or exposed token could affect repositories beyond the intended scope.

Mitigation: Use a least-privilege token limited to the target repositories and actions needed for this skill.

Risk: Insecure endpoint configuration or logged process details can expose token-bearing requests.

Mitigation: Set GITEA_URL to an HTTPS endpoint you control, avoid broad account tokens, and rotate any token previously used with HTTP or in environments where process arguments are visible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qizhou-guo/skills/gitea-actions)
- [Publisher profile](https://clawhub.ai/user/qizhou-guo)

## Skill Output:

**Output Type(s):** [JSON, API calls, Shell commands, Configuration]

**Output Format:** [JSON-compatible status and workflow-run data, with environment-variable configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITEA_URL and GITEA_TOKEN environment variables.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
