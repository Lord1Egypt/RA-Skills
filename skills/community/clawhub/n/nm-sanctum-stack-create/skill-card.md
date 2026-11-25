## Description:

Initializes a stacked branch set from an ordered plan, one branch per slice with parent-child links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when a plan has two or more dependent changes, creating an ordered local branch stack so each slice is based on the preceding slice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some reported actions may not create or verify the promised branch stack.

Mitigation: Review the proposed slices and confirm the branch parent links and final topology before relying on the stack.

Risk: The broad ‘pr’ trigger could activate unexpectedly.

Mitigation: Invoke the skill explicitly when working on a plan that needs an ordered branch stack.

## Reference(s):

- [Sanctum plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-stack-create)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local branch stack with one branch per ordered plan slice.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
