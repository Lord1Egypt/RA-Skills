## Description:

PDCA workflow automation with session binding and progress recovery. Requires Python 3.6 and Git (optional).

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucezhu888](https://clawhub.ai/user/brucezhu888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to break complex work into PDCA plans, track checklist progress, recover interrupted work, and archive completed plan files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plan files and progress checks can expose saved session IDs, task names, and filenames.

Mitigation: Use a dedicated workspace, avoid real session IDs or sensitive task names in shared plan files, and review progress output before sharing it.

Risk: Commands that accept paths can operate outside the documented plan workspace.

Mitigation: Run the skill only in the intended workspace and avoid absolute paths or parent-directory paths in plan commands.

Risk: Archive and cleanup actions can move or delete archived plan files.

Mitigation: Require user confirmation for archive and cleanup, and use cleanup --dry-run before deleting files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucezhu888/skills/plan-do-check-act)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, console status text, shell command examples, and plan.md-style task files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can create, update, pause, resume, archive, and clean up plan files through bundled Python scripts.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
