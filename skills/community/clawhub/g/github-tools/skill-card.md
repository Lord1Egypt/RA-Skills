## Description:

Interact with GitHub using the `gh` CLI for issues, pull requests, CI runs, and advanced API queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[164149043](https://clawhub.ai/user/164149043)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query GitHub issues, pull requests, workflow runs, and API data with the GitHub CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent using this skill may rely on the caller's existing GitHub CLI login, which can permit write actions if later prompted.

Mitigation: Confirm repository targets and review impactful gh commands before approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/164149043/skills/github-tools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the caller's existing gh CLI authentication and repository access.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
