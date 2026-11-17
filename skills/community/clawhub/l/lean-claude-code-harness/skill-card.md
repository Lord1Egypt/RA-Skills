## Description:

Use when building, auditing, or simplifying an AI coding-agent harness, especially when the current runtime has unclear config precedence, weak tool permissions, hidden product-only behavior, or poor transcriptability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aznikline](https://clawhub.ai/user/aznikline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, simplify, or audit Claude Code-style coding-agent harnesses. It focuses reviews on explicit configuration precedence, permission-aware tool execution, file-backed skill discovery, transcript persistence, and a visible query loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisted transcripts may capture prompts, tool steps, final responses, or secrets if recording is enabled without privacy controls.

Mitigation: Document transcript storage, retention, deletion, redaction, and file permissions, and allow users to disable or scope recording for sensitive sessions.

Risk: Harness guidance can be applied incompletely, leaving config precedence, permission modes, skill discovery, session persistence, or the query loop unverified.

Mitigation: Use the skill's minimal verification checklist before treating the harness as usable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aznikline/skills/lean-claude-code-harness)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with checklists and implementation plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a minimal harness shape, kept and removed layers, config precedence, permission model, and verification plan.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
