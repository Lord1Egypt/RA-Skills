## Description:

Interact with GitHub using the `gh` CLI for issues, pull requests, CI runs, and advanced GitHub API queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrherojack](https://clawhub.ai/user/mrherojack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate GitHub repositories through the GitHub CLI, including issue triage, pull request checks, workflow run inspection, and structured API queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub CLI commands run with the user's authenticated GitHub permissions.

Mitigation: Review proposed commands that create, modify, merge, close, or delete GitHub data before execution.

Risk: Commands may target the wrong repository when run outside the intended working directory.

Mitigation: Use `--repo owner/repo` or direct GitHub URLs when repository context is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrherojack/skills/github-custom)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub CLI commands and JSON filtering examples using `--json` and `--jq`.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
