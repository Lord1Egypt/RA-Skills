## Description:

Systematic protocol for working through a project build queue (NEXT_TASKS.md), including task selection, execution, verification, checkpointing, and handoff across agent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to guide an agent through an ordered project build queue with explicit setup, testing, verification, checkpointing, and session handoff steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow mandates automatic commits and broad staging, which can record unintended local changes.

Mitigation: Require human review before staging or committing files, and stage only files that were intentionally changed for the current task.

Risk: The workflow includes hard-coded SSH and local HTTP delegation steps for a named environment.

Mitigation: Remove or gate outbound SSH and curl commands unless the target host and delegation service are explicitly trusted for the deployment environment.

Risk: The workflow calls an external enforcement script whose behavior is not fully described in the artifact.

Mitigation: Inspect and verify the enforcement script separately before allowing an agent to execute it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rmbell09-lang/skills/lucky-build-protocol)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with checklists and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs project workflow steps, verification gates, logging, commits, and handoff notes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
