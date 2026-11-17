## Description:

A Chinese novel-review skill that audits completed chapters for reader payoff density, narrative quality, setting consistency, character plausibility, and produces scores, issue lists, and revision suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao-zwl](https://clawhub.ai/user/zhao-zwl)

### License/Terms of Use:

MIT-0

## Use Case:

Authors, editors, and writing agents use this skill to review completed Chinese novel chapters, score narrative quality and reader payoff, identify continuity and craft issues, and prioritize revisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct broad code-driven manuscript edits and memory-file synchronization without strong scoping or rollback safeguards.

Mitigation: Require an explicit chapter or file scope, ask for a proposed diff or dry run before edits, and keep backups before approving bulk Python edits or memory-file synchronization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhao-zwl/skills/novel-chapter-review)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown review reports with score tables, issue lists, revision priorities, and proposed manuscript changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scoped manuscript-edit proposals, validation steps, and batch-edit commands when the user approves revisions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
