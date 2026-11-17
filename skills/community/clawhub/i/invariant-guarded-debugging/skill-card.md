## Description:

Guard diagnosis and repair with falsifiable hypotheses, executable invariants, verified guard integrity, semantic boundaries, state-drift checks, rollback, adversarial checks, and trajectory resets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinguy](https://clawhub.ai/user/pinguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to diagnose and repair software issues while preserving known-good behavior, honoring protected boundaries, and avoiding path-dependent or schema-only fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to propose diagnostic checks or repairs that affect live systems, protected files, or service state.

Mitigation: Keep normal review and approval for privileged, destructive, out-of-scope, or persistent actions, and require executable invariants plus rollback evidence before mutation.

Risk: A guard can provide false confidence if it observes the wrong path, stale state, empty inputs, or a different runtime instance.

Mitigation: Validate guard integrity by confirming the exact observed object, checking that the guard can fail meaningfully, and using canaries when operational behavior matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pinguy/skills/invariant-guarded-debugging)
- [Server-resolved GitHub provenance](https://github.com/pinguy/Skills/tree/main/skills/invariant-guarded-debugging)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with checklists, report templates, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces diagnostic structure, acceptance checks, rollback criteria, and completion or blocked report formats.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
