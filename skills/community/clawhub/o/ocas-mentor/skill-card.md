## Description:

Mentor orchestrates long-running multi-skill workflows, evaluates journaled skill performance, compares champion and challenger variants, and proposes skill improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use Mentor to coordinate long-running projects, run heartbeat evaluations over skill journals, and route improvement proposals or variant decisions to companion skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mentor can run recurring background jobs, read OpenClaw journals, invoke companion skills, and write orchestration or evaluation state.

Mitigation: Review scheduled jobs and heartbeat registration before use; disable background entries that are not needed and monitor generated journals and intake files.

Risk: The release evidence reports a silent self-update path from a mutable GitHub source.

Mitigation: Disable or remove the automatic self-update schedule unless updates are reviewed and approved before installation.

Risk: The bundled contact-enrichment workflow may process Gmail history and write personal facts to Weave.

Mitigation: Review each plan before execution, avoid scheduled random contact enrichment, and require confidence thresholds before personal data is written.

## Reference(s):

- [Mentor README](README.md)
- [Mentor Orchestration Engine](references/orchestration_engine.md)
- [Mentor Evaluation Engine](references/evaluation_engine.md)
- [Mentor Evolution Engine](references/evolution_engine.md)
- [Mentor Workflow Plans](references/workflow_plans.md)
- [Mentor Schemas](references/schemas.md)
- [Mentor Journal](references/journal.md)
- [Contact Enrichment Plan](references/plans/contact-enrichment.plan.md)
- [ClawHub Skill Page](https://clawhub.ai/indigokarasu/skills/ocas-mentor)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and structured JSON files with occasional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local project state, journals, evaluation records, workflow plan state, and intake files for companion skills.]

## Skill Version(s):

2.3.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
