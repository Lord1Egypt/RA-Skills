## Description:

Pushes all branches in a stack and opens or updates one dependent PR per slice. Use after stack-create to publish the stack or after adding commits to a slice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after creating a committed branch stack or adding commits to publish stack branches, open or maintain a dependent pull request for each slice, and post a stack summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad push scope may publish bookmarks outside the requested stack, and the scan reports mismatches between advertised and reported behavior.

Mitigation: Review the selected branches and publication targets before running; confirm the resulting pull requests and stack summary.

Risk: The security scan was partial because one static analysis was degraded by a parser limit.

Mitigation: Review the skill’s behavior and publication scope before installing.

## Reference(s):

- [Sanctum plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)
- [ClawHub skill listing](https://clawhub.ai/athola/skills/nm-sanctum-stack-push)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Git and GitHub CLI operations with a Markdown stack summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an existing committed stack and authenticated GitHub CLI; pushes branches and posts a stack summary.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
