## Description:

Reviews motor engineering drawings for pole-slot matching, dimensions, technical requirements, GD&T, tolerances, and review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongjie666888](https://clawhub.ai/user/yongjie666888)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and motor engineers use this skill to review motor engineering drawings and produce structured issue reports and checklist files for human engineering signoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checklist and review report content may be mistaken for automated CAD or PDF validation.

Mitigation: Treat outputs as review aids only and keep human engineering signoff before accepting drawing changes.

Risk: The bundled checklist script can create a local text file when --output is supplied.

Mitigation: Use --output only with an intentional destination path.

## Reference(s):

- [Motor Drawing GD&T Reference](references/gdt-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/yongjie666888/skills/motor-drawing-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional plain-text checklist files from the bundled Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The checklist script can write a text file when the user supplies --output.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
