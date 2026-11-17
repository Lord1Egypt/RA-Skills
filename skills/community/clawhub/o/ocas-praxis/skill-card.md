## Description:

Ocas Praxis records outcomes, extracts micro-lessons from repeated patterns, consolidates them into capped active behavior shifts, applies active shifts at runtime, and generates plain-language debriefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Ocas Praxis to record task outcomes, derive traceable behavioral lessons, manage a capped set of active behavior shifts, and generate runtime briefs or debriefs for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can maintain persistent behavioral lessons and inject active behavior shifts into future runs.

Mitigation: Install only when persistent behavioral refinement is intended, and review proposed shifts before activation.

Risk: Trusted input, approval, retention, and instruction-precedence controls are not clear enough for a behavior-changing skill.

Mitigation: Use a dedicated permission-limited OCAS_ROOT, keep the intake directory writable only by trusted producers, and periodically delete or archive journals and records that may contain sensitive task context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/indigokarasu/skills/ocas-praxis)
- [Praxis Data Model](references/data_model.md)
- [Praxis Runtime Rules](references/runtime_rules.md)
- [Praxis Debrief Templates](references/debrief_templates.md)
- [Journal](references/journal.md)
- [Praxis Lesson Extraction Rules](references/lesson_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance and JSON-compatible records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce runtime briefs, debriefs, events, lessons, behavior shifts, decisions, and action journals.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
