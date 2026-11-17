## Description:

Spec-first execution workflow for OpenClaw that turns large, vague, or messy project requests into phased, verifiable implementation plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cirokk](https://clawhub.ai/user/cirokk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, rescue, refactor, redesign, and complete medium or large project work with phased execution, acceptance criteria, and incremental verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad project changes, including cleanup, integration, or removal of duplicate paths.

Mitigation: Review proposed file removals and integration changes before accepting them, and verify each meaningful step with the strongest available check.

Risk: Project materials may contain secrets, private URLs, or credentials.

Mitigation: Keep sensitive project data out of reusable or public skill content and review outputs before sharing them.

Risk: The workflow may distinguish simulated integrations from real runtime integrations, but users still need to confirm implementation status.

Mitigation: Require explicit status reporting for what works, what was verified, what remains, and what is blocked externally.

## Reference(s):

- [Acceptance Checklist](artifact/references/acceptance-checklist.md)
- [Execution Template](artifact/references/execution-template.md)
- [ClawHub Skill Page](https://clawhub.ai/cirokk/skills/gsdclaw)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Concise natural-language guidance, status summaries, implementation plans, and task-specific code or shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill with no required credentials, external APIs, special binaries, or hidden execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
