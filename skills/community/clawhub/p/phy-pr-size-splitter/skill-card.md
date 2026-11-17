## Description:

Pull request size analyzer and split planner that measures diff stats, classifies PR size, detects independent logical chunks, and proposes a split plan with branch names, dependency order, and a ready-to-post PR comment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to evaluate whether a GitHub PR or local branch is reviewable and to generate a concrete plan for splitting oversized changes into smaller, ordered PRs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect the current repository or a specified GitHub PR through local git and gh context.

Mitigation: Invoke it explicitly for intended repositories or PRs and review the repository or PR scope before allowing analysis.

Risk: Generated git, gh pr create, or PR-comment actions could affect branches, pull requests, or public review discussion if executed or posted without review.

Mitigation: Review generated commands and comment text before running them or allowing the agent to post them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-pr-size-splitter)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with PR size analysis, split checklist, suggested branch names, dependency order, and optional git or gh commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ready-to-post PR comment text and proposed commands that should be reviewed before execution.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
