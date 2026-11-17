## Description:

Cascades a rebase through an entire PR stack after a base PR merges or upstream changes

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to rebase a published pull request branch stack when its base changes, then update affected branches and pull request bases. It guides conflict handling and verification of the resulting stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that actions may publish or change repository and pull-request state in ways that do not match the stated stacked-rebase purpose.

Mitigation: Review the planned rebase, branch pushes, and pull-request base changes before execution, and confirm each action matches the intended stack update.

Risk: Rebasing rewrites branch history and pushing updated slices may affect remote work or leave pull-request reviews stale.

Mitigation: Confirm the stack branches and remote state, inspect the rebased commits, use the documented --force-with-lease guard, and verify pull-request bases and review status afterward.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-sanctum-stack-rebase)
- [Homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell code blocks and a progress checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that rebase branches, push updated branches, and edit pull request bases.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
