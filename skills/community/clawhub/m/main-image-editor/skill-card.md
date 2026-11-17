## Description:

Orchestrate screenshot + Chinese instruction into PSD batch edits with transaction rollback by reusing psd-automator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhrxy](https://clawhub.ai/user/dhrxy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Chinese screenshot-based editing requests into PSD or PSB text edit batches, preview low-confidence work, and export PNG or ZIP deliverables through psd-automator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite local PSD or PSB design files and the security summary notes rollback and temporary-file handling weaknesses.

Mitigation: Run dry-run first, review resolved targets and proposed edits, and keep independent backups before forced execution.

Risk: The skill reads provided screenshots and resolves PSD or PSB files through a local index, which may expose sensitive project names, copy, or source files.

Mitigation: Use it only with screenshots and design files approved for this workflow, and avoid shared machines or indexes containing sensitive unrelated projects.

Risk: Batches that edit the same PSD more than once can be harder to review and recover from.

Mitigation: Review same-file batches carefully, split high-risk edits into smaller runs, and prefer dry-run or confirmation thresholds before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dhrxy/skills/main-image-editor)

## Skill Output:

**Output Type(s):** [JSON, Files]

**Output Format:** [JSON execution result with PSD edit status and generated PNG or ZIP file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run, low-confidence confirmation, rollback_all failure handling, and optional bundled exports.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
