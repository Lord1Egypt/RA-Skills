## Description:

Pushes all branches in a stack and opens or updates one dependent PR per slice. Use after stack-create to publish the stack or after adding commits to a slice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after creating a stack of branches, or after adding commits to a slice, to push the stack and open or update a dependent pull request for each slice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the `jj` shortcut may publish eligible bookmarks beyond the selected stack, and that observed behavior does not fully match the skill's stated purpose.

Mitigation: Review the suspicious verdict before use; inspect the eligible bookmarks and configured remote, confirm which branches should be published, and review the resulting pull requests and stack summary.

Risk: The security evidence says scanner coverage is incomplete because inspection was partial and the tool-misuse analyzer was degraded.

Mitigation: Review the full skill instructions and commands before installation or execution, and do not treat the partial scan as a clean result.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-sanctum-stack-push)
- [Sanctum plugin homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Shell commands, GitHub pull request updates, Markdown summary]

**Output Format:** [Shell commands and GitHub pull request updates, with a Markdown stack summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an initialized stack with commits on each slice and an authenticated gh CLI; draft pull requests are the default.]

## Skill Version(s):

1.10.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
