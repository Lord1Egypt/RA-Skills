## Description:

Guides agents to make precise code edits by reading target context first, applying minimal replacements, and self-checking changes after editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill when modifying existing files, fixing bugs, refactoring, or changing code logic while keeping diffs small and reviewable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested code edits may still be incorrect or incomplete even though the artifact is low risk.

Mitigation: Review the resulting diff and run relevant type checks, lint, or tests before relying on changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-edit)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown guidance with code-editing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No required binaries; guides read-edit-review workflows and validation handoff.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
