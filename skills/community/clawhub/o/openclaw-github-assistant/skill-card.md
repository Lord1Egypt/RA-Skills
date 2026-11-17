## Description:

Query and manage GitHub repositories - list repos, check CI status, create issues, search repos, and view recent activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorkenn](https://clawhub.ai/user/conorkenn)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to inspect GitHub repositories, check CI status, search repositories, review recent activity, and create issues, repositories, or pull requests from an assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create GitHub issues, repositories, and pull requests using the user's token without clear built-in confirmation.

Mitigation: Review the skill before installation and enable it only where assistant-created GitHub changes are acceptable.

Risk: A broad GitHub token can grant access beyond the repositories needed for the intended workflow.

Mitigation: Use the narrowest token scope possible, preferring public_repo when private repository access is not required.

Risk: Pull-request creation is available even though the main documentation does not fully disclose it.

Mitigation: Treat pull-request creation as an enabled capability during review, policy approval, and runtime monitoring.

## Reference(s):

- [GitHub Personal Access Tokens](https://github.com/settings/tokens)
- [GitHub REST API](https://api.github.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and structured GitHub API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GitHub credentials via GITHUB_TOKEN and GITHUB_USERNAME or matching OpenClaw configuration.]

## Skill Version(s):

2.0.1 (source: server release metadata and skill implementation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
