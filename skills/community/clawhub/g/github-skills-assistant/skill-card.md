## Description:

Query and manage GitHub repositories - list repos, check CI status, create issues, search repos, and view recent activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to let an assistant inspect GitHub repositories, check CI status, search repositories, review recent commits, and create repository resources such as issues, repositories, and pull requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad GitHub token can allow high-impact write actions, including issue, repository, and pull request creation.

Mitigation: Use a fine-grained GitHub token scoped only to the specific repositories and permissions required for the intended workflow.

Risk: The implementation exposes pull request creation that is not disclosed in the main documentation.

Mitigation: Review available actions before installation and disable or restrict workflows that should not create pull requests.

Risk: Stored or shared GitHub credentials can expose repository access.

Mitigation: Store tokens in environment variables, OpenClaw configuration, or a managed secret store, and rotate tokens if compromise is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yesong-hue/skills/github-skills-assistant)
- [GitHub API](https://api.github.com)
- [GitHub Personal Access Tokens](https://github.com/settings/tokens)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Structured JSON-like action results and concise Markdown summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated GitHub API responses may include repository metadata, CI run status, commit summaries, issue URLs, repository URLs, and pull request URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package/index metadata report 2.0.0 and 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
