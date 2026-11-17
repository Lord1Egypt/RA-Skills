## Description:

Git workflow assistant. Generates commit messages, PR descriptions, branch management suggestions, and automates common Git operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local Git changes and produce commit message suggestions, PR description drafts, and branch workflow guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository diffs can contain sensitive code, credentials, or unreleased product details.

Mitigation: Review generated commit messages and PR descriptions before sharing them outside the repository team.

Risk: The documentation advertises smart commit and branch deletion workflows that are not implemented in the packaged commands.

Mitigation: Use the skill as a local Git inspection and drafting helper until mutating workflows include clear previews and confirmation.

## Reference(s):

- [Conventional Commits](https://www.conventionalcommits.org/)
- [OpenClaw Git Workflow on ClawHub](https://clawhub.ai/michealxie001/skills/openclaw-gitflow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from local Git repository state and may include file paths, commit summaries, and branch names.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
