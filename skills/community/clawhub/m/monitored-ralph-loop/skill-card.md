## Description:

Generate copy-paste bash scripts for Ralph Wiggum/AI agent loops (Codex, Claude Code, OpenCode, Goose).

This skill is ready for commercial/non-commercial use.

## Publisher:

[endogen](https://clawhub.ai/user/endogen)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to set up monitored AI coding loops that plan work, execute implementation iterations, run backpressure checks, and notify OpenClaw or a human when decisions, errors, blockers, or completion events occur.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports autonomous coding loops that can run unattended with reduced safeguards.

Mitigation: Run the loop only in a disposable branch, container, virtual machine, or otherwise constrained workspace, and review generated commits before pushing or merging.

Risk: Documented setup paths include host-level persistent changes such as systemd services, swap configuration, and fstab edits.

Mitigation: Do not run those commands unless host persistence is intentional and the operator knows how to disable or roll back the changes.

Risk: Claude defaults may use permission-bypass behavior when RALPH_FLAGS is not set explicitly.

Mitigation: Set safe RALPH_FLAGS explicitly before running Claude-based loops.

## Reference(s):

- [Monitored Ralph Loop on ClawHub](https://clawhub.ai/endogen/skills/monitored-ralph-loop)
- [Ralph pattern](https://ghuntley.com/ralph/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project setup files, loop commands, notification formats, and mode-specific planning or building guidance.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
