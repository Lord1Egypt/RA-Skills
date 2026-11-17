## Description:

Automated refactoring assistant for Python symbol renames, code-smell suggestions, and backup-based undo workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect projects for refactoring opportunities, preview Python symbol renames, apply selected renames, and restore backed-up files when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify project files more broadly or less safely than advertised.

Mitigation: Use it only on version-controlled test projects, review the plan first, and inspect diffs before committing changes.

Risk: Running rename execution without preview may make unintended edits.

Mitigation: Run with --dry-run first and proceed only after the affected files and occurrences are acceptable.

Risk: Disabling backups or restoring from an untrusted backup ID can make recovery unreliable.

Mitigation: Avoid --no-backup and use only trusted backup IDs when invoking undo.

Risk: Advertised refactoring commands and safety guarantees do not fully match the shipped implementation.

Mitigation: Treat unsupported commands as unavailable and verify behavior on disposable test projects before using the skill on important code.

## Reference(s):

- [OpenClaw Refactoring release page](https://clawhub.ai/michealxie001/skills/oc-refactoring)
- [Publisher profile](https://clawhub.ai/user/michealxie001)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify project files when rename execution is run without --dry-run; backup and undo behavior should be verified before use.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
