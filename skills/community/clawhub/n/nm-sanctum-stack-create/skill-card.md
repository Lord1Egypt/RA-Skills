## Description:

Initializes a stacked branch set from an ordered plan, one branch per slice with parent-child links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn a plan with sequentially dependent changes into a verified stack of branches, with each branch based on the preceding slice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial and reports a mismatch between the stated purpose and the behavior it examined.

Mitigation: Review the version-control actions and consider whether the scan coverage gap is acceptable before installing.

Risk: Creating and switching branches changes the repository's version-control state.

Mitigation: Confirm the clean working tree, base branch, and ordered slices before running the commands, then verify the resulting branch topology.

## Reference(s):

- [Related Sanctum project homepage (metadata link)](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Branch names and stack topology depend on the user's ordered plan and base branch.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
