## Description:

Ramps implementation ambition a notch only after the prior increment is understood

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to break work they need to understand and maintain into small implementation increments, then increase scope only after demonstrating understanding of the prior increment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner coverage is partial because a referenced hook file could not be resolved.

Mitigation: Review the complete plugin and resolve or inspect the referenced hook before installation; the clean scanner result is not a guarantee of safety.

Risk: Applying the ramp process to trivial edits can add unnecessary ceremony.

Mitigation: Skip the process for single bounded edits, trivial reversible changes, and generated or vendored code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-imbue-graduated-implementation)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)
- [Advancement Gate](modules/advancement-gate.md)
- [Ramp Ledger](modules/ramp-ledger.md)
- [Research Basis: Graduated Implementation](modules/research-basis.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands]

**Output Format:** [Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Incremental workflow guidance with checks selected according to project stakes.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
