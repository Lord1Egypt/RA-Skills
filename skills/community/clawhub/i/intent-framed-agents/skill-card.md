## Description:

Frames coding-agent work sessions with explicit intent capture and drift monitoring. Use when a session transitions from planning/Q&A to implementation for coding tasks, refactors, feature builds, bug fixes, or other multi-step execution where scope drift is a risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pskoett](https://clawhub.ai/user/pskoett)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to create an explicit intent frame before non-trivial implementation work, monitor scope drift during execution, and close the work with a concise resolution record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions use unpinned third-party commands that can install mutable or broader content than the reviewed skill file.

Mitigation: Review the exact source before installing, prefer a pinned commit or release, and use the specific skill path unless intentionally installing the whole repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pskoett/skills/intent-framed-agents)
- [Entire CLI](https://github.com/entireio/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown intent frames, checks, and resolutions with optional shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured session artifacts for intent capture, drift checks, and task resolution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
