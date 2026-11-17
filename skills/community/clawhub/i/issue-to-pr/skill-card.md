## Description:

issue-to-pr automatically fixes GitHub issues end-to-end by reading the issue, analyzing repository code, implementing a fix, and preparing a pull request for user-approved submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4ydx3906](https://clawhub.ai/user/4ydx3906)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn GitHub issue references into investigated, locally implemented fixes and review-ready pull requests. It is intended for workflows where an agent can inspect code, run project checks, and wait for user approval before pushing or creating a PR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act through the user's GitHub account to fork repositories, push branches, and create pull requests.

Mitigation: Run it only with GitHub permissions you are comfortable using, and review the diff and PR body before approving push or PR creation.

Risk: Generated pull request text may include an unrelated promotional footer.

Mitigation: Review the final PR body and remove the footer before allowing PR creation when it is not appropriate.

Risk: Installing from an untrusted or moving source could place unwanted instructions in the local skills directory.

Mitigation: Use a trusted or pinned installer path and review the installer before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/4ydx3906/skills/issue-to-pr)
- [GitHub CLI documentation](https://cli.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, code diffs, commit messages, and pull request text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify repository files locally and may prepare GitHub commits, pushes, forks, and pull requests after user approval.]

## Skill Version(s):

1.3.0 (source: frontmatter, clawhub.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
