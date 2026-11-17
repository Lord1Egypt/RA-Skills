## Description:

Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent produce GitHub CLI guidance for inspecting issues, pull requests, CI workflow runs, logs, and GitHub API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to use existing GitHub CLI authentication for repository actions that create, modify, delete, or post content.

Mitigation: Review any state-changing gh command before approval, and use explicit --repo owner/repo values or URLs to avoid acting on the wrong repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/nidhov01-github)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
