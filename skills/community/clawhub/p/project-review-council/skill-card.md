## Description:

Project Review Council guides an agent through a Chinese-default, evidence-tagged project review using staged evidence collection, role audits, adversarial cross-review, risk ranking, business evaluation, and Go/No-Go decision memos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run structured project audits, investment reviews, launch readiness checks, quarterly reviews, and Go/No-Go decisions. It is intended for evidence-based project evaluation across strategy, technology, product, security, growth, finance, competition, and execution perspectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Several optional resources referenced by the workflow, including role files, checklists, weights, and an executive-summary template, were not included in the inspected package.

Mitigation: Confirm those resources are available before a full audit, or adapt the workflow to the included role configuration, rubrics, role-report template, and decision-memo template.

Risk: Project judgments can be incomplete or misleading when supplied project evidence is sparse or unverified.

Mitigation: Use the skill's evidence tags, unknown-information handling, and rollback steps to separate evidence from assumptions before making decisions.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/qomob/project-review-council)
- [ClawHub skill page](https://clawhub.ai/qomob/skills/project-review-council)
- [Skill definition](artifact/SKILL.md)
- [Role configuration](artifact/config/roles.yaml)
- [Global settings](artifact/config/settings.yaml)
- [Phase 1 project understanding workflow](artifact/workflows/01-understand.md)
- [Phase 3 role audit workflow](artifact/workflows/03-role-audit.md)
- [Phase 9 decision workflow](artifact/workflows/09-decision.md)
- [Phase 10 red-blue workflow](artifact/workflows/10-red-blue.md)
- [Scoring rubric](artifact/rubrics/scoring.md)
- [Risk-level rubric](artifact/rubrics/risk-level.md)
- [Decision matrix](artifact/rubrics/decision-matrix.md)
- [Role report template](artifact/templates/role-report.md)
- [Decision memo template](artifact/templates/decision-memo.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown reports, tables, scorecards, decision memos, and evidence-tagged role reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-default output with strict evidence tags, staged checkpoints, and no executable code.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
