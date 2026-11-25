## Description:

Cascades a rebase through an entire PR stack after a base PR merges or upstream changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to rebase a published pull request stack after its base merges, upstream changes, or a middle slice is revised, then update affected branches and pull request bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review marks this release suspicious, citing publishing beyond the selected pull request stack and behavior that may not consistently match the stated rebasing purpose.

Mitigation: Before running its publishing steps, inspect the target branches and confirm that no unrelated or unpublished work will be sent to a remote.

## Reference(s):

- [Sanctum plugin page](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-sanctum-stack-rebase)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Git and GitHub CLI commands]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata; artifact frontmatter lists 1.10.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
