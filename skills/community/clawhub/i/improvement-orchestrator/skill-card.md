## Description:

Coordinates a full skill-improvement pipeline that proposes, scores, optionally evaluates, applies, gates, and retries changes for one or more target skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to run an end-to-end improvement cycle across one or more skills, including proposal generation, scoring, optional evaluation, execution, gate decisions, and retry feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify installed skill files during execution.

Mitigation: Run it only on version-controlled targets, use a dedicated state directory, and review generated diffs, receipts, and rollback pointers before accepting changes.

Risk: The security summary warns that requested evaluation may not be a mandatory safety gate.

Mitigation: Do not rely on --task-suite alone for approval; require manual review or separate smoke tests before promoting generated changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/improvement-orchestrator)
- [Architecture](references/architecture.md)
- [Guardrails](references/guardrails.md)
- [End-to-End Demo](references/end-to-end-demo.md)
- [Phases](references/phases.md)
- [Adapters](references/adapters.md)
- [Skill-Evaluator Adapter](references/skill-evaluator-adapter.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON artifacts, Markdown diffs, and concise terminal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local state, trace, execution, and gate receipt files under the configured state root.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
