## Description:

Query and manage GitHub repositories - list repos, check CI status, create issues, search repos, and view recent activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyzx](https://clawhub.ai/user/gyzx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to query repository details, monitor GitHub Actions status, search repositories, and create GitHub issues, repositories, or pull requests from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated GitHub write actions can create repositories, issues, and pull requests.

Mitigation: Use a fine-grained token limited to selected repositories and required permissions, and require explicit user approval before write actions.

Risk: Pull-request creation is exposed by the artifact but is not clearly documented in the public skill instructions.

Mitigation: Gate or disable pull-request creation until reviewers confirm it is intended and documented.

Risk: GitHub tokens can grant broad repository access if over-scoped or mishandled.

Mitigation: Store tokens in environment variables or a credential store, avoid committing them, and rotate tokens after suspected exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gyzx/skills/openclaw-github-assistant-2-0-1)
- [Publisher profile](https://clawhub.ai/user/gyzx)
- [GitHub token setup](https://github.com/settings/tokens)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration guidance]

**Output Format:** [Text or Markdown summaries of GitHub API results, plus links to created GitHub objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GitHub credentials through GITHUB_TOKEN/GITHUB_USERNAME or github.token/github.username configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact implementation reports 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
