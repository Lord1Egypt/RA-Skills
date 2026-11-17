## Description:

Automatically detects and heals locked OpenClaw session files, clears stale locks, and recovers failed sessions after lock timeout errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to diagnose OpenClaw session lock errors, clear stale lock files, unlock specific sessions, and recover corrupted session JSONL files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool can delete OpenClaw session lock files, including active locks when force options are used.

Mitigation: Run dry-run checks first, stop active OpenClaw processes before unlocking or healing, and avoid force options unless the active process state has been verified.

Risk: The recovery command can modify session JSONL files while removing corrupted lines.

Mitigation: Use exact session IDs and keep backups before recovery; confirm the recovered session contents before continuing work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neckr0ik/skills/neckr0ik-session-healer)
- [SKILL.md](artifact/SKILL.md)
- [healer.py](artifact/scripts/healer.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with CLI command examples and terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run local repair commands that inspect, delete, or rewrite OpenClaw session files.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, artifact/claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
