## Description:

Automated refactoring assistant for Python code that previews and applies symbol renames, reports refactoring suggestions, and manages backups for undo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Python code for refactoring opportunities, preview symbol renames, apply selected rename operations, and restore changes from generated backups when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rename and undo operations can rewrite or restore files more broadly than the documentation implies.

Mitigation: Use the skill only on a backed-up Git working tree, start with narrow target roots, run dry-run previews first, and inspect diffs before committing changes.

Risk: Undo can restore files from an unintended backup when the backup ID is not verified.

Mitigation: List available backups first and use only a backup ID that was created by the refactoring operation you intend to reverse.

Risk: Advertised extract, inline, move, and batch features may be unreliable or unavailable in the current artifact.

Mitigation: Treat those advertised features as unsupported until the implementation is fixed; rely on the exposed rename, suggest, undo, and list-backups commands.

## Reference(s):

- [OpenClaw Refactoring ClawHub skill page](https://clawhub.ai/michealxie001/skills/openclaw-refactoring)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rewrite Python files and create backup files under .refactoring/backup when rename operations are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
