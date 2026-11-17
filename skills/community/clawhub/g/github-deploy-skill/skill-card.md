## Description:

Commit and push local project changes to GitHub, with optional repo creation and deployment hints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cruciata](https://clawhub.ai/user/cruciata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare and run a Windows PowerShell workflow that commits local Git changes, pushes to a selected branch, optionally creates a GitHub repository, and prints deployment hints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised PowerShell script is not included in the artifact, so the commit, push, remote configuration, and repository creation behavior cannot be verified from this release.

Mitigation: Do not run the documented commands until the exact github-deploy-skill.ps1 file has been obtained from a trusted source and reviewed.

Risk: The described workflow can use authenticated Git and GitHub CLI credentials to push code or create repositories.

Mitigation: Run it only in the intended repository and account context after reviewing the pending git diff, target remote, branch, and GitHub authentication state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cruciata/skills/github-deploy-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/cruciata)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create commits, change git remotes, push branches, or create GitHub repositories when executed with authenticated local tools.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
