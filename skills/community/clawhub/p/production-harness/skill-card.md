## Description:

Production Harness provides an adaptive engineering workflow for coding agents that combines task complexity grading, planning, verification, review, checkpointing, and multi-agent failure analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christianye](https://clawhub.ai/user/christianye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to structure feature work, bug fixes, reviews, debugging, and shipping workflows with explicit quality gates. It is most relevant for multi-step software development tasks where planning, verification evidence, and controlled subagent coordination matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session-history inspection can expose unrelated private conversation data.

Mitigation: Limit inspection to the failed subagent's error metadata and avoid adding unrelated transcripts or sensitive content to the active task.

## Reference(s):

- [Production Harness on ClawHub](https://clawhub.ai/christianye/skills/production-harness)
- [Checkpoint Patterns for Agent Systems](references/checkpoint-patterns.md)
- [MAST Failure Taxonomy for Multi-Agent Systems](references/mast-failure-taxonomy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance and verification expectations; no direct code execution is required by the skill itself.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
