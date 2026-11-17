## Description:

Novel Outliner - 大纲解析器 parses plain text, JSON, or Markdown novel outlines into per-chapter writing prompts and a chapter summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shine8592](https://clawhub.ai/user/shine8592)

### License/Terms of Use:

MIT-0

## Use Case:

Authors and developers use this skill to convert structured novel outlines into per-chapter prompt files and a JSON chapter summary for downstream writing workflows. It does not write or expand the novel itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outline content may contain instruction-like text that is copied into generated prompts.

Mitigation: Use trusted outlines or review generated prompts before sending them to an agent with sensitive tools or data access.

Risk: Generated prompts force Chinese-only novel-writing constraints that may not fit every writing workflow.

Mitigation: Confirm the downstream writing task requires these constraints before using the generated prompt files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shine8592/skills/novel-outliner)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Per-chapter text prompt files plus a JSON chapter summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated prompts include Chinese-only writing constraints and may copy outline text into downstream prompts.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
