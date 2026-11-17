## Description:

Helps OpenClaw agents extract, search, reconcile, archive, and monitor memory across sessions, with local processing by default and an opt-in cloud extraction path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mistermijarvis](https://clawhub.ai/user/mistermijarvis)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to maintain agent memory, retrieve relevant facts, resolve contradictions, and review memory health over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory and session content may be sensitive, and optional cloud extraction can transmit sanitized excerpts off the machine.

Mitigation: Review memory before use; set TRACE_LLM_LOCAL_ONLY=1 for sensitive content and avoid cloud credentials or TRACE_LLM_ALLOW_CLOUD=1 unless transmission is acceptable.

Risk: Scheduled maintenance, indexing, and --force, --apply, or --fix commands can alter memory or ontology data.

Mitigation: Review commands before running them, start with read-only or dry-run modes where available, and keep backups before enabling changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mistermijarvis/skills/memory-toolkit)
- [Toolkit documentation](artifact/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands; invoked tools can return text or JSON and update local memory files and indexes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only memory queries and audit reports are available; maintenance commands may modify local memory.]

## Skill Version(s):

4.0.6 (source: ClawHub release, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
