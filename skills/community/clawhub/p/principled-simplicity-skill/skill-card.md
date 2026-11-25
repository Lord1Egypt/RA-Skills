## Description:

Diagnoses recurring failures and recommends reusable mechanisms or abstractions instead of accumulating patches, guided by evidence and evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longfellow1](https://clawhub.ai/user/longfellow1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate repeated failures and choose an appropriate response, from a case fix to a reusable rule, mechanism, or abstraction. It guides that decision with evidence about recurrence, logic spread, evaluation, and regressions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner notes a low-severity concern about evaluative guidance; recommendations may not fit every project's goals or evaluation criteria.

Mitigation: Check that the skill's guidance fits the project's goals, and validate proposed changes against project-specific evidence and evaluations before adopting them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/longfellow1/skills/principled-simplicity-skill)
- [GitHub source repository](https://github.com/Longfellow1/Principled-Simplicity-skill)
- [Procedure](references/procedure.md)
- [Failure patterns](references/patterns.md)
- [Decision heuristics](references/heuristics.md)
- [Abstraction readiness](references/abstraction-readiness.md)
- [Prompt decomposition](references/prompt-decompose.md)
- [Patch audit](references/patch-audit.md)
- [Deep fix scan script](references/deep-fix-scan.py)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Conversational text or structured Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a failure diagnosis, response options, a mechanism recommendation, and an evaluation plan.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
