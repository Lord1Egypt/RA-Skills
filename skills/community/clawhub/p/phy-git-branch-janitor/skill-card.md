## Description:

Git branch cleanup assistant that audits local and remote branches, categorizes merged, stale, orphaned, and active branches, and produces a prioritized cleanup plan with shell commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review Git branch state, identify branches that can be safely removed, and prepare cleanup commands for local and remote branches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated branch deletion commands can be unsafe for unusual branch names or repositories with branches created by other people.

Mitigation: Review commands before running them, validate and shell-quote branch names, and confirm remote deletions or force-deletes manually.

Risk: Stale unmerged branches may contain work that has not been preserved elsewhere.

Mitigation: Confirm with the branch owner or PR status before using force-delete commands for unmerged branches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-git-branch-janitor)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes categorized branch findings and cleanup commands that should be reviewed before execution.]

## Skill Version(s):

1.0.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
