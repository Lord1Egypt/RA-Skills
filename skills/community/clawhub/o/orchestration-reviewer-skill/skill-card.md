## Description:

Reviews existing workflow plans in Plan IR format and returns structured decisions, issues, scorecards, and revision suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow operators use this skill to review existing orchestration plans for goal alignment, topology soundness, skill binding, scope safety, executability, complexity, and governance risks before execution or revision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan verdict is suspicious because the skill overstates some safety checks and uses unpinned Python dependencies.

Mitigation: Use the review output as advisory only, pin dependencies before operational use, and independently enforce dependency, expression, manifest-scope, and sensitive-field validation in the workflow engine.

Risk: Review results can influence workflow execution decisions but are not an execution approval gate.

Mitigation: Require human review for high-risk revisions or reject decisions, and re-run static validation on any revised Plan IR before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tuobadaidai/skills/orchestration-reviewer-skill)
- [Publisher Profile](https://clawhub.ai/user/tuobadaidai)
- [Review Manual](references/review-manual.md)
- [Review Rules](references/review-rules.md)
- [Scoring Policy](references/scoring-policy.md)
- [Security Guardrails](references/security-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Structured JSON review results with human-readable issue summaries and optional revised Plan IR or diff reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include overall_decision, confidence, scorecard, issues, suggested_actions, validation_report, revised_plan_ir, and diff_report.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
