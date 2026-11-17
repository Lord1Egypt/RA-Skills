## Description:

Control PowerPoint app sessions, slides, notes, export, and presentation state with osascript workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to control a live Microsoft PowerPoint session on macOS when the task depends on the current open deck, slide state, notes, slideshow state, or PowerPoint's own export behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables local automation of Microsoft PowerPoint through osascript, including actions that can alter open presentations.

Mitigation: Install only where local PowerPoint automation is intended, identify the exact presentation before changes, and require explicit confirmation for destructive actions.

Risk: Persistent workspace routing or memory notes could affect future agent behavior beyond the immediate task.

Mitigation: Approve any persistent routing text before adding it and keep ~/powerpoint/ memory limited to non-sensitive environment facts, safety defaults, and reusable recovery notes.

Risk: The PDF export example can be unsafe with untrusted filenames or paths.

Mitigation: Use trusted absolute export paths, avoid overwrites without confirmation, and harden path handling before using the export pattern with untrusted input.

## Reference(s):

- [ClawHub PowerPoint Skill](https://clawhub.ai/ivangdavila/skills/powerpoint)
- [PowerPoint Skill Homepage](https://clawic.com/skills/powerpoint)
- [Setup Guide](artifact/setup.md)
- [Execution Matrix](artifact/execution-matrix.md)
- [Live Control Patterns](artifact/live-control-patterns.md)
- [Safety Checklist](artifact/safety-checklist.md)
- [Troubleshooting](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and AppleScript command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Microsoft PowerPoint, and osascript; may create or use local memory under ~/powerpoint/.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
