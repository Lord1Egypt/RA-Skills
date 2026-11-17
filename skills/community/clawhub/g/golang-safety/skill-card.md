## Description:

Defensive Golang coding to prevent panics, silent data corruption, and subtle runtime bugs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review and improve Go code for nil-safety, slice and map aliasing, numeric conversion overflow, resource lifecycle issues, zero-value design, and related defensive coding concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad repository-level Git command access and agent delegation beyond what normal Go safety guidance clearly needs.

Mitigation: Install only when comfortable granting those capabilities, and prefer versions that narrow Git usage to read-only inspection commands or clearly document when mutating Git operations and delegation may occur.

## Reference(s):

- [Nil Safety Deep Dive](artifact/references/nil-safety.md)
- [Slice and Map Safety Deep Dive](artifact/references/slice-map-safety.md)
- [Project homepage](https://github.com/samber/cc-skills-golang)
- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-safety)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Go code examples and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets Go source files; command-based checks require the Go toolchain when used.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
