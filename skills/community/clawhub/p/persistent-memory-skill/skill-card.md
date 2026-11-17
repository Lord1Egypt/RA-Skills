## Description:

Use when a user wants cross-session personal context shared by compatible AI agents, or asks to load, save, inspect, archive, recover, clean up, or upgrade local memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainypilgrimage-beep](https://clawhub.ai/user/rainypilgrimage-beep)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let compatible local AI agents share reviewed personal context through plain Markdown files. It supports loading baseline context, saving confirmed updates, and safely managing archive, delete, recovery, health, and summary-first on-demand memory workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext local memory can expose sensitive context to other trusted compatible agents on the same filesystem.

Mitigation: Do not save passwords, API keys, credentials, or sensitive material that should not be readable by another trusted local agent.

Risk: Save, archive, delete, and recover operations can change local memory files if the user confirms an incorrect proposal.

Mitigation: Review the proposed content, source path, destination path, index changes, and recovery effect before giving explicit confirmation.

Risk: Summary-first loading can omit details that exist only in the full memory file.

Mitigation: Use the summary only when it is sufficient; when a requested fact is absent, ambiguous, or needs exact support, read the full file before answering.

Risk: Cross-agent sharing fails when agents do not resolve the same local memory path or lack read/write permission.

Mitigation: Use this skill only with compatible agents that can access the same local filesystem path for ~/.persistent-memory/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rainypilgrimage-beep/skills/persistent-memory-skill)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)
- [v0.8 Summary-First Prototype Results](artifact/docs/experiments/v08-summary-first-results.md)
- [v0.8 Summary-First Loading Implementation Plan](artifact/docs/superpowers/plans/2026-07-15-v08-summary-first-release.md)
- [Architecture diagram](artifact/architecture.svg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown and plain text responses, including proposed memory file content and lifecycle previews.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before writing or moving local memory files; memory is stored as plaintext on the same local filesystem.]

## Skill Version(s):

0.8.0 (source: evidence.release.version and CHANGELOG.md, released 2026-07-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
