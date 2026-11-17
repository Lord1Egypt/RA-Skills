## Description:

A portable agent playbook for quality-controlling scientific manuscripts that need reliable DOCX/PDF export of math, figures, tables, and submission packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xutaoguo55](https://clawhub.ai/user/xutaoguo55)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, research assistants, and manuscript-preparation agents use this skill to inspect source manuscripts, rebuild DOCX/PDF outputs, check formula rendering, validate figures and tables, and synchronize final submission packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells agents to update its own persistent instructions when they discover reusable manuscript QC lessons, which could introduce incorrect or misleading guidance without review.

Mitigation: Require proposed skill updates to be written to a separate review file or patch for human approval before SKILL.md is modified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xutaoguo55/skills/manuscript-math-docx-qc)
- [Skill workflow](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration]

**Output Format:** [Markdown guidance with inline shell commands, checklists, and source-edit recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be verified against generated DOCX/PDF artifacts and local tool availability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
