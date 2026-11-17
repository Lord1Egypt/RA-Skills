## Description:

Self-Evolving Agent (Lorin) helps AI coding agents capture errors, user corrections, feature requests, and repeatable workflows as structured learnings that can be reviewed, promoted, or extracted into reusable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lorinwei](https://clawhub.ai/user/lorinwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run a self-improvement loop for AI coding agents: logging command failures, corrections, requested capabilities, and useful discoveries, then promoting proven patterns into reusable instructions or skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning records can retain private data, secrets, or incorrect guidance across sessions.

Mitigation: Review and sanitize learning entries before storage, and require explicit approval before promoting entries into instruction files or new skills.

Risk: Global hook configuration can apply the workflow more broadly than intended across projects.

Mitigation: Prefer project-local hooks, use narrow matchers, and enable PostToolUse error detection only where command-output review is acceptable.

Risk: The artifact includes deletion guidance using an rm -rf pattern for obsolete skills.

Mitigation: Replace destructive deletion with archival or manual removal, and review the target path before removing any skill directory.

Risk: Error detection reads command output that may contain sensitive values.

Mitigation: Treat command output as sensitive and avoid logging or forwarding raw output unless the user explicitly approves that detail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lorinwei/skills/lorin-self-evolving-agent)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, hook configuration snippets, and generated skill or learning-file scaffolds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .learnings entries, SKILL.md scaffolds, and project-local hook configuration when explicitly applied.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
