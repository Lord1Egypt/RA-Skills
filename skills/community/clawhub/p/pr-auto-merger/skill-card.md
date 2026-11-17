## Description:

Autonomous PR merge agent that scans GitHub repositories for approved, CI-passing, mergeable pull requests and can merge them automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanxevo3](https://clawhub.ai/user/lanxevo3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps teams use this skill to identify pull requests that appear ready to merge, preview them in dry-run mode, and optionally run scheduled or manual GitHub CLI merges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can merge pull requests automatically with the permissions of the authenticated GitHub CLI token.

Mitigation: Default to dry-run review, verify the script before live use, and run with tightly scoped GitHub credentials.

Risk: Approval-count behavior should not be treated as a complete policy control.

Mitigation: Enforce required approvals, status checks, and merge restrictions with GitHub branch protection rules.

Risk: The artifact's GitHub Actions example includes a package-install step for gh that security guidance flags as unsuitable.

Mitigation: Use a trusted GitHub CLI installation path and validate the runtime environment before scheduled live merges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanxevo3/skills/pr-auto-merger)
- [Publisher profile](https://clawhub.ai/user/lanxevo3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute GitHub CLI merge operations when configured outside dry-run mode.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
