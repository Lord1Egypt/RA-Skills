## Description:

AI Workflow Enforcer inspired by the Steam game "The King Is Watching" that structures agent work into sequential, checkpointed workflows with progress reporting and task translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d0roro](https://clawhub.ai/user/d0roro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to break large or long-running requests into ordered workflow steps, checkpoint progress, emit progress reports, and reduce skipped work during batch execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found that advertised workflow enforcement and verification may be unreliable for real side-effecting automation.

Mitigation: Use only for experiments or tightly controlled local workflows, and require human review before relying on results for downloads, reports, compliance evidence, or other consequential tasks.

Risk: Natural-language translate-and-run behavior can produce or execute plans that do not provide real verification or safe resume semantics.

Mitigation: Preview generated plans, use bounded inputs and safe state paths, and validate completion with independent checks before treating work as complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/d0roro/skills/kingswatching)
- [README](artifact/README.md)
- [User Guide](artifact/USER_GUIDE.md)
- [Installation Guide](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and Python-oriented guidance with optional shell commands and structured workflow results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe sequential execution plans, progress reporting, heartbeat configuration, checkpoint resume behavior, and verification settings.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and setup.py report 0.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
